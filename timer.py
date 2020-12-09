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
        return
    with source_ar(source_name) as source, data_ar() as settings:
        timer = datetime.now(timezone.utc) - started_at
        obs.obs_data_set_string(settings, "text", str(timer)[:9])
        obs.obs_source_update(source, settings)

def refresh_pressed(props, prop):
    update_text()



# ------------------------------------------------------------

def script_description():
    return "Updates a text source to the text retrieved from a URL at every specified interval.\n\nBy Jim"

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
    
    if (race != obs.obs_data_get_string(settings, "race")):
        race = obs.obs_data_get_string(settings, "race")
        r = racetime_client.get_race(race)

    if not r:
        print (f"error in url {url}")
    elif source_name != "":
        started_at = r.started_at
        obs.timer_add(update_text, interval)

#def script_defaults(settings):
#	obs.obs_data_set_default_int(settings, "interval", 30)

def script_properties():
    props = obs.obs_properties_create()

    p = obs.obs_properties_add_list(props, "race", "Race", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    races = racetime_client.get_races()
    if races is not None:
        for race in races:
            print(f"race {race.name} is currently {race.status}")
            obs.obs_property_list_add_string(p, race.name, race.name)
            #if race.status.value.lower() in { "open", "invitational", "in_progress" }:
            #    obs.obs_property_list_add_string(p, race.name, race.name)

    p = obs.obs_properties_add_list(props, "race", "Race", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)

    p = obs.obs_properties_add_list(props, "source", "Text Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            if source_id == "text_gdiplus" or source_id == "text_ft2_source":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)

        obs.source_list_release(sources)

    obs.obs_properties_add_button(props, "button", "Refresh", refresh_pressed)
    return props
