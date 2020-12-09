import string
import obspython as obs
import urllib.parse
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from string import Template
import racetime_client
from models.race import Race, RaceCategory
import asyncio


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

url         = ""
started_at = None
interval    = 100
source_name = ""
full_name   = "Matkap#6663"
category    = ""
race        = ""

# ------------------------------------------------------------

def update_text():
    """takes scripted_text , sets its value in obs  """
    if started_at is None:
        time = "-0:00:15.0"
    else:
        timer = datetime.now(timezone.utc) - started_at
        time = str(timer)[:9]
    with source_ar(source_name) as source, data_ar() as settings:
        obs.obs_data_set_string(settings, "text", time)
        obs.obs_source_update(source, settings)

def refresh_pressed(props, prop):
    # TODO update list of races
    #update_text()
    None



# ------------------------------------------------------------

def script_description():
    return "Select a text source to use as your timer and enter your full" + \
    "username on racetime.gg  (including discriminator). This only needs" + \
    "to be done once.\n\nThen select the race room each race you join and" + \
    "stop worrying about whether you started your timer or not."

def script_update(settings):
    global url
    global interval
    global source_name
    global started_at
    global category
    global race
    global full_name

    obs.timer_remove(update_text)
    
    source_name = obs.obs_data_get_string(settings, "source")
    
    r = None
    if (race != obs.obs_data_get_string(settings, "race")):
        race = obs.obs_data_get_string(settings, "race")
        print(f"race is {race}\n")
        r = racetime_client.get_race(race)

    if r is not None and source_name != "":
        started_at = r.started_at
        obs.timer_add(update_text, interval)

#def script_defaults(settings):
#	obs.obs_data_set_default_int(settings, "interval", 30)

def script_properties():
    props = obs.obs_properties_create()

    p = obs.obs_properties_add_list(props, "source", "Text Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    with source_list_ar() as sources:
        if sources is not None:
            for source in sources:
                source_id = obs.obs_source_get_unversioned_id(source)
                if source_id == "text_gdiplus" or source_id == "text_ft2_source":
                    name = obs.obs_source_get_name(source)
                    print(f"{name}\n")
                    obs.obs_property_list_add_string(p, name, name)

    obs.obs_properties_add_text(props, "username", "Username", obs.OBS_TEXT_DEFAULT)

    p = obs.obs_properties_add_list(props, "race", "Race", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    races = racetime_client.get_races()
    if races is not None:
        for race in races:
            obs.obs_property_list_add_string(p, race.name, race.name)

    p = obs.obs_properties_add_list(props, "race", "Race", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)

    obs.obs_properties_add_button(props, "button", "Refresh", refresh_pressed)
    return props
