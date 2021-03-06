import asyncio
from asyncio.events import get_event_loop
from datetime import datetime, timezone
import pytest
from unittest.mock import Mock

from models.chat_message import ChatMessage

from gadgets.media_player import MediaPlayer

from races_for_testing import get_test_race
from users_for_testing import get_test_entrant, get_test_entrants


@pytest.mark.asyncio
async def test_entrant_finished_first(random_users):
    event_loop = get_event_loop()
    event_loop.set_debug(True)

    play_media = Mock()
    media_player = MediaPlayer()
    media_file_path = "fake/path/test.mp3"
    media_player.play_media_callback = play_media
    media_player.add_trigger(
        media_file_path, 0)
    media_player.monitoring_type = 0
    await asyncio.sleep(0.1)

    assert len(media_player.triggers) == 1
    play_media.assert_not_called()

    entrant = get_test_entrant(
        status_value="in_progress", user=next(random_users))
    entrants = get_test_entrants(random_users, entrant)
    race = get_test_race(entrants=entrants)
    media_player.race_updated(race, entrant.user.full_name)
    await asyncio.sleep(0.1)
    play_media.assert_not_called()

    entrant = race.get_entrant_by_name(entrant.user.full_name)
    await asyncio.sleep(0.1)
    entrant.place = 1
    entrant.status.value = "finished"
    entrant.finish_time = datetime.now(timezone.utc)
    media_player.race_updated(race, entrant.user.full_name)
    await asyncio.sleep(0.1)
    play_media.assert_called_once_with(
        media_file_path, 0)


@pytest.mark.asyncio
async def test_bot_chat_message():
    event_loop = get_event_loop()
    event_loop.set_debug(True)
    play_media = Mock()
    media_player = MediaPlayer()
    media_file_path = "fake/path/test.mp3"
    media_player.play_media_callback = play_media
    media_player.add_chat_trigger(media_file_path, False, True)
    media_player.monitoring_type = 0
    await asyncio.sleep(0.1)
    assert len(media_player.chat_triggers) == 1

    c = ChatMessage(
        "123456", None, None, datetime.now(timezone.utc), " ", " ",
        False, False, False
    )

    media_player.chat_updated(c)
