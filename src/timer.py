import string
import obspython as obs
import urllib.parse
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from string import Template
import racetime_client
from models.race import Race, RaceCategory
import asyncio
from threading import Thread
import time


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
started_at              = None
finish_time             = None
source_name             = ""
full_name               = ""
category                = ""
race                    = ""
race_status_value       = ""
entrant_status_value    = ""
check_race_updates      = False
close_thread            = False
start_delay             = None

# ------------------------------------------------------------

def update_text():
    """takes scripted_text , sets its value in obs  """

    if race_status_value == "open" or race_status_value == "invitational":
        time = "-" + str(start_delay) + ".0"
    elif finish_time is not None:
        time = str(finish_time)[:9]
    elif entrant_status_value == "dnf" or entrant_status_value == "dq" \
    or race_status_value == "cancelled":
        time = "--:--:--.-"
    elif started_at is not None:
        timer = datetime.now(timezone.utc) - started_at
        if race_status_value == "pending":
            time = "-0:00:{:2.1f}".format(timer.total_seconds())[1:5]
        else:
            time = str(timer)[:9]
    else:
        return
    with source_ar(source_name) as source, data_ar() as settings:
        obs.obs_data_set_string(settings, "text", time)
        obs.obs_source_update(source, settings)

def race_updater():
    while True:
        if close_thread:
            break
        time.sleep(5.0)
        if check_race_updates:
            r = None
            r = racetime_client.get_race(race)
            if r is not None:
                update_race(r)

def update_race(r: Race):
    global race
    global finish_time
    global check_race_updates
    global race_status_value
    global entrant_status_value
    global started_at
    global start_delay

    started_at = r.started_at
    start_delay = r.start_delay
    race_status_value = r.status.value
    entrant = next((x for x in r.entrants if x.user.full_name == full_name), None)
    if entrant is not None:
        if entrant.finish_time:
            finish_time = entrant.finish_time
        entrant_status_value = entrant.status.value


def refresh_pressed(props, prop, *args, **kwargs):
    p = obs.obs_properties_get(props, "source")
    fill_source_list(p)
    p = obs.obs_properties_get(props, "race")
    fill_race_list(p)
    return True

def new_race_selected(props, prop, settings):
    race = obs.obs_data_get_string(settings, "race")
    r = racetime_client.get_race(race)
    if r is not None:
        update_race(r)
        obs.obs_data_set_default_string(settings, "race_info", r.info)
    else:
        obs.obs_data_set_default_string(settings, "race_info", "Race not found")
    return True

# ------------------------------------------------------------

def script_description():
    return "Select a text source to use as your timer and enter your full " + \
    "username on racetime.gg  (including discriminator). This only needs " + \
    "to be done once.\n\nThen select the race room each race you join and " + \
    "stop worrying about whether you started your timer or not."

def script_load(settings):
    race_update_t = Thread(target=race_updater)
    race_update_t.daemon = True
    race_update_t.start()

def script_unload():
    close_thread = True

def script_update(settings):
    global source_name
    global race
    global full_name
    global check_race_updates

    obs.timer_remove(update_text)
    
    source_name = obs.obs_data_get_string(settings, "source")

    race = obs.obs_data_get_string(settings, "race")

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

def fill_race_list(p):
    obs.obs_property_list_clear(p)
    obs.obs_property_list_add_string(p, "", "")
    races = racetime_client.get_races()
    if races is not None:
        for race in races:
            obs.obs_property_list_add_string(p, race.name, race.name)

def script_properties():
    props = obs.obs_properties_create()

    p = obs.obs_properties_add_list(props, "source", "Text Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    fill_source_list(p)

    obs.obs_properties_add_text(props, "username", "Username", obs.OBS_TEXT_DEFAULT)

    p = obs.obs_properties_add_list(props, "race", "Race", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    fill_race_list(p)
    obs.obs_property_set_modified_callback(p, new_race_selected)

    p = obs.obs_properties_add_text(props, "race_info", "Race Desc", obs.OBS_TEXT_MULTILINE)
    obs.obs_property_set_enabled(p, False)

    refresh = obs.obs_properties_add_button(props, "button", "Refresh", lambda *props: None)
    obs.obs_property_set_modified_callback(refresh, refresh_pressed)
    return props
