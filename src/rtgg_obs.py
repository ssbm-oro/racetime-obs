import json
import websockets
from websockets.client import WebSocketClientProtocol
import obspython as obs
from datetime import datetime, timedelta, timezone
import racetime_client
from models.race import Race, race_from_dict
import asyncio
import websockets
import dateutil
import logging
from helpers.LogFormatter import LogFormatter
from helpers.obs_context_manager import source_ar, source_list_ar, data_ar
from gadgets.timer import Timer
from gadgets.coop import Coop
from gadgets.qualifier import Qualifier

def script_description():
    return "<p>You've loaded the incorrect script.<br><br>Please remove this file and add 'racetime_obs.py' instead</p>"

class RacetimeObs():
    logger = logging.Logger("racetime-obs")
    race: Race = None
    selected_race = ""
    check_race_updates = False
    race_changed = False
    full_name = ""
    category = ""
    timer = Timer()
    coop = Coop()
    qualifier = Qualifier()

    def update_sources(self):
        if self.race is not None:
            if self.timer.enabled:
                color, time = self.timer.get_timer_text(self.race, self.full_name)
                self.set_source_text(self.timer.source_name, time, color)
            if self.coop.enabled:
                self.set_source_text(self.coop.source_name, self.coop.text, None)
                self.set_source_text(self.coop.label_source_name, self.coop.label_text, None)
            if self.qualifier.enabled:
                self.set_source_text(self.qualifier.qualifier_par_source, self.qualifier.qualifier_par_text, None)
                self.set_source_text(self.qualifier.qualifier_score_source, self.qualifier.entrant_score, None)
            pass

    def race_update_thread(self):
        self.logger.debug("starting race update")
        race_event_loop = asyncio.new_event_loop()
        race_event_loop.run_until_complete(self.race_updater())
        race_event_loop.run_forever()


    async def race_updater(self):
        headers = {
            'User-Agent': "oro-obs-bot_alpha"
        }
        host = "racetime.gg"

        while True:
            if not self.timer.enabled:
                await asyncio.sleep(5.0)
            else:
                if self.race is None and self.selected_race != "":
                    self.race = racetime_client.get_race(self.selected_race)
                if self.race is not None and self.race.websocket_url != "":
                    async with websockets.connect("wss://racetime.gg" + self.race.websocket_url, host=host, extra_headers=headers) as ws:
                        self.race_changed = False
                        self.logger.info(
                            f"connected to websocket: {self.race.websocket_url}")
                        await self.process_messages(ws)
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
                if datetime.now(timezone.utc) - last_pong > timedelta(seconds=20):
                    await ws.send(json.dumps({"action": "ping"}))
            except websockets.ConnectionClosed:
                self.logger.error(f"websocket connection closed")
                self.race = None
                break

    def process_ws_message(self, data, last_pong):
        if data.get("type") == "race.data":
            r = race_from_dict(data.get("race"))
            self.logger.debug(f"race data parsed: {r}")
            self.logger.debug(f"current race is {self.race}")
            if r is not None and r.version > self.race.version:
                self.race = r
                self.logger.debug(f"self.race is {self.race}")
                self.coop.update_coop_text(self.race, self.full_name)
                self.qualifier.update_qualifier_text(self.race, self.full_name)
        elif data.get("type") == "pong":
            last_pong = dateutil.parser.parse(data.get("date"))
            pass
        return last_pong


    def update_logger(self, enabled: bool, log_to_file: bool, log_file: str, level: str):
        self.logger.disabled = not enabled
        self.logger.handlers = []
        handler = logging.StreamHandler()
        if log_to_file:
            try:
                handler = logging.FileHandler(log_file)
            except:
                self.logger.error(f"Unable to open {log_file}")
        elif level == "Debug":
            handler.setLevel(logging.DEBUG)
        elif level == "Info":
            handler.setLevel(logging.INFO)
        else:
            handler.setLevel(logging.ERROR)
        handler.setFormatter(LogFormatter())
        self.logger.addHandler(handler)

    @staticmethod
    def fill_source_list(p):
        obs.obs_property_list_clear(p)
        obs.obs_property_list_add_string(p, "", "")
        with source_list_ar() as sources:
            if sources is not None:
                for source in sources:
                    source_id = obs.obs_source_get_unversioned_id(source)
                    if source_id == "text_gdiplus" or source_id == "text_ft2_source":
                        name = obs.obs_source_get_name(source)
                        obs.obs_property_list_add_string(p, name, name)

    def fill_race_list(self, race_list, category_list):
        obs.obs_property_list_clear(race_list)
        obs.obs_property_list_clear(category_list)
        obs.obs_property_list_add_string(category_list, "All", "All")

        obs.obs_property_list_add_string(race_list, "", "")
        races = racetime_client.get_races()
        if races is not None:
            categories = []
            for race in races:
                if self.category == "" or self.category == "All" or race.category.name == self.category:
                    obs.obs_property_list_add_string(
                        race_list, race.name, race.name)
                if not race.category.name in categories:
                    categories.append(race.category.name)
                    obs.obs_property_list_add_string(
                        category_list, race.category.name, race.category.name)


    def fill_coop_entrant_lists(self, props):
        self.fill_entrant_list(obs.obs_properties_get(props, "coop_partner"))
        self.fill_entrant_list(obs.obs_properties_get(props, "coop_opponent1"))
        self.fill_entrant_list(obs.obs_properties_get(props, "coop_opponent2"))


    def fill_entrant_list(self, entrant_list):
        obs.obs_property_list_clear(entrant_list)
        obs.obs_property_list_add_string(entrant_list, "", "")
        if self.race is not None:
            for entrant in self.race.entrants:
                obs.obs_property_list_add_string(
                    entrant_list, entrant.user.full_name, entrant.user.full_name)
    
    
    # copied and modified from scripted-text.py by UpgradeQ

    @staticmethod
    def set_source_text(source_name: str, text: str, color: int):
        with source_ar(source_name) as source, data_ar() as settings:
            obs.obs_data_set_string(settings, "text", text)
            source_id = obs.obs_source_get_unversioned_id(source)
            if color is not None:
                if source_id == "text_gdiplus":
                    obs.obs_data_set_int(settings, "color", color)  # colored text

                else:  # freetype2,if taken from user input it should be reversed for getting correct color
                    number = "".join(hex(color)[2:])
                    color = int("0xff" f"{number}", base=16)
                    obs.obs_data_set_int(settings, "color1", color)
            
            obs.obs_source_update(source, settings)