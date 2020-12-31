import asyncio
from asyncio.events import AbstractEventLoop
import json
import logging
from datetime import datetime, timedelta, timezone

import dateutil
import websockets
from websockets.client import WebSocketClientProtocol
from websockets.exceptions import ConnectionClosedError

import clients.racetime_client as racetime_client
from gadgets.coop import Coop
from gadgets.ladder_timer import LadderTimer
from gadgets.qualifier import Qualifier
from gadgets.timer import Timer
from gadgets.media_player import MediaPlayer
from helpers.LogFormatter import LogFormatter
from models.race import Race, race_from_dict
from models.chat_message import chat_message_from_dict


def script_description():
    return (
        "<p>You've loaded the incorrect script.<br><br>Please remove this file"
        "and add 'racetime_obs.py' instead</p>"
    )


class RacetimeObs():
    logger = logging.Logger("racetime-obs")
    race: Race = None
    selected_race = "None"
    check_race_updates = False
    race_changed = False
    full_name = ""
    category = ""
    timer = Timer()
    coop = Coop()
    qualifier = Qualifier()
    media_player: MediaPlayer = None
    ladder_timer: LadderTimer = None
    event_loop: AbstractEventLoop = None

    def __init__(self):
        self.event_loop = asyncio.get_event_loop()
        self.timer.logger = self.logger
        self.coop.logger = self.logger
        self.qualifier.logger = self.logger
        self.media_player = MediaPlayer()
        self.media_player.logger = self.logger
        self.ladder_timer = LadderTimer()
        self.ladder_timer.logger = self.logger

    def race_update_thread(self):
        self.logger.debug("starting race update")
        self.event_loop.run_until_complete(self.race_updater())
        self.event_loop.run_forever()

    async def race_updater(self):
        headers = {
            'User-Agent': "oro-obs-bot_alpha"
        }
        host = "racetime.gg"

        while True:
            if not self.timer.is_enabled():
                await asyncio.sleep(5.0)
            else:
                if self.race is None and self.selected_race != "None":
                    self.race = (
                        racetime_client.get_race_by_name(self.selected_race)
                    )
                    self.logger.debug("got race, trying to connect to ws")
                if self.race is not None and self.race.websocket_url != "":
                    self.logger.debug("received race, trying to connect to ws")
                    try:
                        async with websockets.connect(
                            "wss://racetime.gg" + self.race.websocket_url,
                            host=host, extra_headers=headers
                        ) as ws:
                            self.race_changed = False
                            self.logger.info(
                                "connected to websocket:"
                                " {self.race.websocket_url}"
                            )
                            await self.process_messages(ws)
                    except (ConnectionRefusedError, ConnectionClosedError):
                        self.logger.error("websocket closed unexpectedly.")
                        continue
            await asyncio.sleep(5.0)

    async def process_messages(self, ws: WebSocketClientProtocol):
        last_pong = datetime.now(timezone.utc)
        while True:
            try:
                if self.race_changed:
                    self.logger.info("new race selected")
                    self.race_changed = False
                    break
                message = await asyncio.wait_for(ws.recv(), 5.0)
                self.logger.info(f"received message from websocket: {message}")
                data = json.loads(message)
                last_pong = self.process_ws_message(data, last_pong)
            except asyncio.TimeoutError:
                await self.ping_ws(ws, last_pong)
                continue
            except websockets.ConnectionClosed:
                self.logger.error("websocket connection closed")
                self.race = None
                break

    async def ping_ws(self, ws: WebSocketClientProtocol, last_pong: datetime):
        if datetime.now(timezone.utc) - last_pong > timedelta(seconds=20):
            await ws.send(json.dumps({"action": "ping"}))

    def process_ws_message(self, data: dict, last_pong: datetime):
        if data.get("type") == "race.data":
            self.update_race(data)
        elif data.get("type") == "chat.message":
            self.process_chat_message(data.get("message"))
        elif data.get("type") == "pong":
            last_pong = dateutil.parser.parse(data.get("date"))
            pass
        return last_pong

    def process_chat_message(self, data: dict):
        message = chat_message_from_dict(data)
        self.logger.debug(
                f"received chat message. chat sounds enabled is "
                f"{self.media_player.ping_chat_messages}"
            )
        if (
                self.media_player.ping_chat_messages and
                message.is_bot or message.highlight
        ):
            self.logger.debug(
                    f"trying to play {self.media_player.chat_media_file}")
            self.event_loop.call_soon_threadsafe(
                    self.media_player.play_media_callback,
                    self.media_player.chat_media_file,
                    self.media_player.monitoring_type
                )

    def update_race(self, data: dict):
        r = race_from_dict(data.get("race"))
        self.logger.debug(f"race data parsed: {r}")
        self.logger.debug(f"current race is {self.race}")
        if r is not None and r.version > self.race.version:
            self.race = r
            self.logger.debug(f"self.race is {self.race}")
            self.coop.update_coop_text(self.race, self.full_name)
            self.qualifier.update_qualifier_text(self.race, self.full_name)
            self.event_loop.call_soon_threadsafe(
                    self.media_player.race_updated,
                    self.race, self.full_name)

    def update_logger(
        self, enabled: bool, log_to_file: bool, log_file: str, level: str
    ):
        self.logger.disabled = not enabled
        self.logger.handlers = []
        handler = logging.StreamHandler()
        if log_to_file:
            try:
                handler = logging.FileHandler(log_file)
            except IOError as e:
                self.logger.error(f"IOError while opening open {log_file}:")
                self.logger.error(f"{e.errno} {e.strerror}")
        elif level == "Debug":
            handler.setLevel(logging.DEBUG)
        elif level == "Info":
            handler.setLevel(logging.INFO)
        else:
            handler.setLevel(logging.ERROR)
        handler.setFormatter(LogFormatter())
        self.logger.addHandler(handler)
