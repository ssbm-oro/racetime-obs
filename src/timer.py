import json
import string

import websockets
import obspython as obs
import urllib.parse
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import racetime_client
from models.race import Race, RaceCategory, race_from_dict
import asyncio
from asyncio import AbstractEventLoop
from threading import Thread
import time
from websockets import WebSocketClientProtocol
import ssl


# auto release context managers
@contextmanager
def source_ar(source_name):
    source = obs.obs_get_source_by_name(source_name)
    try:
        yield source
    finally:
        obs.obs_source_release(source)


@contextmanager
def p_source_ar(id, source_name, settings):
    try:
        _source = obs.obs_source_create_private(id, source_name, settings)
        yield _source
    finally:
        obs.obs_source_release(_source)


@contextmanager
def data_ar(source_settings=None):
    if not source_settings:
        settings = obs.obs_data_create()
    if source_settings:
        settings = obs.obs_source_get_settings(source_settings)
    try:
        yield settings
    finally:
        obs.obs_data_release(settings)


@contextmanager
def scene_ar(scene):
    scene = obs.obs_scene_from_source(scene)
    try:
        yield scene
    finally:
        obs.obs_scene_release(scene)


@contextmanager
def filter_ar(source, name):
    source = obs.obs_source_get_filter_by_name(source, name)
    try:
        yield source
    finally:
        obs.obs_source_release(source)

@contextmanager
def source_list_ar():
    source_list = obs.obs_enum_sources()
    try:
        yield source_list
    finally:
        obs.source_list_release(source_list)

# ------------------------------------------------------------

url                     = ""
source_name             = ""
full_name               = ""
category                = ""
race                    = None
selected_race           = ""
check_race_updates      = False
close_thread            = False
use_podium_colors       = False
pre_color               = 0xFFFFFF
racing_color            = 0xFFFFFF
first_color             = 0xFF0000
second_color            = 0x00FF00
third_color             = 0x0000FF
finished_color          = 0xFFFFFF
race_changed            = False
race_event_loop         = None

# ------------------------------------------------------------

def update_text():
    """takes scripted_text , sets its value in obs  """
    global race
    global full_name
    global entrant

    if not race:
        return

    entrant = next((x for x in race.entrants if x.user.full_name == full_name), None)

    color = None
    if race.status.value == "open" or race.status.value == "invitational":
        time = "-" + str(race.start_delay) + ".0"
        color = pre_color
    elif entrant is not None:
        if entrant.finish_time is not None:
            time = str(entrant.finish_time)[:9]
            if entrant.place == 1:
                color = first_color
            elif entrant.place == 2:
                color = second_color
            elif entrant.place == 3:
                color = third_color
            else:
                color = finished_color
        elif entrant.status.value == "dnf" or entrant.status.value == "dq" \
        or race.status.value == "cancelled":
            time = "--:--:--.-"
            color = 0xFF0000
    elif race.started_at is not None:
        if use_podium_colors:
            color = racing_color
        timer = datetime.now(timezone.utc) - race.started_at
        if timer.total_seconds() < 0.0:
            time = "-0:00:{:04.1f}".format(timer.total_seconds() * -1.0)
        else:
            time = str(timer)[:9]
    else:
        return
    with source_ar(source_name) as source, data_ar() as settings:
        obs.obs_data_set_string(settings, "text", time)
        if use_podium_colors:
            set_color(source, settings, color)
        obs.obs_source_update(source, settings)

def race_update_thread():
    global race_changed
    global race_event_loop

    race_event_loop = asyncio.new_event_loop()
    race_event_loop.run_until_complete(race_updater())
    race_event_loop.run_forever()

# def race_changed():
#     event_loop = asyncio.get_event_loop()
#     event_loop.stop()
#     race_event_loop.run_until_complete(race_updater())
#     race_event_loop.run_forever()

async def race_updater():
    global race
    global race_changed
    global close_thread

    headers = {
        'User-Agent': "oro-obs-bot_alpha"
    }
    host = "racetime.gg"

    while True:
        #print(f"websocket_url is {websocket_url}\n")
        if race is not None and race.websocket_url != "":
            #print(f"new race selected: {race}\n")
            async with websockets.connect("wss://racetime.gg" + race.websocket_url, host=host, extra_headers=headers) as ws:
                #print(f"websocket connected: {websocket_url}\n")
                while True:
                    try:
                        #print(f"race_changed: {race_changed}, close_thread: {close_thread}")
                        if race_changed:
                            race_changed = False
                            break
                        if close_thread:
                            close_thread = False
                            break
                        message = await asyncio.wait_for(ws.recv(), 5.0)
                        #print(f"received message: {message}\n")
                        data = json.loads(message)
                        if data.get("type") == "race.data":
                            #print("race data received\n")
                            r = race_from_dict(data.get("race"))
                            if r is not None:
                                race = r
                        elif data.get("type") == "pong":
                            pass
                            #print("pong!\n")
                    except asyncio.TimeoutError:
                        #print("ping!\n")
                        await ws.send(json.dumps({"action": "ping"}))
                    except websockets.ConnectionClosed:
                        race = None
                        break
        await asyncio.sleep(5.0)


def refresh_pressed(props, prop, *args, **kwargs):
    fill_source_list(obs.obs_properties_get(props, "source"))
    fill_race_list(obs.obs_properties_get(props, "race"), obs.obs_properties_get(props, "category_filter"))
    return True

def new_race_selected(props, prop, settings):
    global race_changed
    global close_thread
    global race
    global selected_race

    selected_race = obs.obs_data_get_string(settings, "race")
    r = racetime_client.get_race(selected_race)
    if r is not None:
        race = r
        obs.obs_data_set_default_string(settings, "race_info", r.info)
        race_changed = True
    else:
        obs.obs_data_set_default_string(settings, "race_info", "Race not found")
        close_thread = True
    return True

def new_category_selected(props, prop, settings):
    global category
    category = obs.obs_data_get_string(settings, "category_filter")
    fill_race_list(obs.obs_properties_get(props, "race"), prop)
    return True

def podium_toggled(props, prop, settings):
    vis = obs.obs_data_get_bool(settings, "use_podium")
    obs.obs_property_set_visible(obs.obs_properties_get(props, "podium_group"), vis)
    return True

# copied and modified from scripted-text.py by UpgradeQ
def set_color(source, settings, color):
    if color is None:
        return
    source_id = obs.obs_source_get_unversioned_id(source)
    if source_id == "text_gdiplus":
        obs.obs_data_set_int(settings, "color", color)  # colored text

    else:  # freetype2,if taken from user input it should be reversed for getting correct color
        number = "".join(hex(color)[2:])
        color = int("0xff" f"{number}", base=16)
        obs.obs_data_set_int(settings, "color1", color)
        #obs.obs_data_set_int(settings, "color2", color)

def loading_finished(event):
    if event == obs.OBS_FRONTEND_EVENT_FINISHED_LOADING:
        race_update_t = Thread(target=race_update_thread)
        race_update_t.daemon = True
        race_update_t.start()

# ------------------------------------------------------------

def script_description():
    return "<center><p>Select a text source to use as your timer and enter your full " + \
    "username on racetime.gg  (including discriminator). This only needs " + \
    "to be done once.\n\nThen select the race room each race you join and " + \
    "stop worrying about whether you started your timer or not.<hr/></p>"

def script_load(settings):
    global use_podium_colors
    use_podium_colors = obs.obs_data_get_bool(settings, "use_podium")

    obs.obs_frontend_add_event_callback(loading_finished)

def script_save(settings):
    obs.obs_data_set_bool(settings, "use_podium", use_podium_colors)

def script_unload():
    global close_thread
    close_thread = True

def script_update(settings):
    global source_name
    global race
    global selected_race
    global category
    global full_name
    global check_race_updates
    global use_podium_colors
    global pre_color
    global first_color
    global second_color
    global third_color
    global racing_color
    global finished_color

    obs.timer_remove(update_text)
    
    source_name = obs.obs_data_get_string(settings, "source")

    selected_race = obs.obs_data_get_string(settings, "race")
    category = obs.obs_data_get_string(settings, "category_filter")

    use_podium_colors = obs.obs_data_get_bool(settings, "use_podium")
    pre_color = obs.obs_data_get_int(settings, "pre_color")
    first_color = obs.obs_data_get_int(settings, "first_color")
    second_color = obs.obs_data_get_int(settings, "second_color")
    third_color = obs.obs_data_get_int(settings, "third_color")
    racing_color = obs.obs_data_get_int(settings, "racing_color")
    finished_color = obs.obs_data_get_int(settings, "finished_color")

    if source_name != "":
        obs.timer_add(update_text, 100)
        check_race_updates = True
    else:
        check_race_updates = False

    full_name = obs.obs_data_get_string(settings, "username")

def script_defaults(settings):
	obs.obs_data_set_default_string(settings, "race_info", "Race info")
	obs.obs_data_set_default_string(settings, "race", "")

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

def fill_race_list(race_list, category_list):
    obs.obs_property_list_clear(race_list)
    obs.obs_property_list_clear(category_list)
    obs.obs_property_list_add_string(category_list, "", "")

    obs.obs_property_list_add_string(race_list, "", "")
    races = racetime_client.get_races()
    if races is not None:
        categories = []
        for race in races:
            if category == "" or race.category.name == category:
                obs.obs_property_list_add_string(race_list, race.name, race.name)
            if not race.category.name in categories:
                categories.append(race.category.name)
                obs.obs_property_list_add_string(category_list, race.category.name, race.category.name)

def script_properties():
    props = obs.obs_properties_create()

    setup_group = obs.obs_properties_create()
    obs.obs_properties_add_group(props, "initial_setup", "Initial setup - Check to make changes", obs.OBS_GROUP_CHECKABLE, setup_group)
    p = obs.obs_properties_add_list(setup_group, "source", "Text Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    fill_source_list(p)
    obs.obs_properties_add_text(setup_group, "username", "Username", obs.OBS_TEXT_DEFAULT)

    category_list = obs.obs_properties_add_list(props, "category_filter", "Filter by Category", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    race_list = obs.obs_properties_add_list(props, "race", "Race", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    fill_race_list(race_list, category_list)
    obs.obs_property_set_modified_callback(race_list, new_race_selected)
    obs.obs_property_set_modified_callback(category_list, new_category_selected)

    p = obs.obs_properties_add_text(props, "race_info", "Race Desc", obs.OBS_TEXT_MULTILINE)
    obs.obs_property_set_enabled(p, False)

    refresh = obs.obs_properties_add_button(props, "button", "Refresh", lambda *props: None)
    obs.obs_property_set_modified_callback(refresh, refresh_pressed)

    p = obs.obs_properties_add_bool(props, "use_podium", "Use custom color for podium finishes?")
    obs.obs_property_set_modified_callback(p, podium_toggled)

    podium_group = obs.obs_properties_create()
    obs.obs_properties_add_group(props, "podium_group", "Podium Colors", obs.OBS_GROUP_NORMAL, podium_group)
    obs.obs_property_set_visible(obs.obs_properties_get(props, "podium_group"), use_podium_colors)

    obs.obs_properties_add_color(podium_group, "pre_color", "Pre-race:")
    obs.obs_properties_add_color(podium_group, "racing_color", "Still racing:")
    obs.obs_properties_add_color(podium_group, "first_color", "1st place:")
    obs.obs_properties_add_color(podium_group, "second_color", "2nd place:")
    obs.obs_properties_add_color(podium_group, "third_color", "3rd place:")
    obs.obs_properties_add_color(podium_group, "finished_color", "After podium:")

    return props
