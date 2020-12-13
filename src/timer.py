import json
import time
import websockets
import obspython as obs
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import racetime_client
from models.race import Race, race_from_dict
import asyncio
from threading import Thread
import websockets
import dateutil
import logging


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

class LogFormatter(logging.Formatter):
    formats = {
        logging.ERROR    : "%(asctime)s - %(levelname)s - %(message)s",
        logging.DEBUG       : "%(asctime)s - %(levelname)s - %(message)s in %(funcName)s line %(lineno)d",
        logging.INFO        : "%(asctime)s - %(levelname)s - %(message)s"
    }
    
    def format(self, record : logging.LogRecord):
        f = logging.Formatter(self.formats.get(record.levelno))
        f.converter = time.gmtime
        return f.format(record)

# ------------------------------------------------------------

logger                  = logging.Logger("racetime-obs")
source_name             = ""
timer_text              = ""
full_name               = ""
category                = ""
race : Race             = None
selected_race           = ""
check_race_updates      = False
use_podium_colors       = False
pre_color               = 0xFFFFFF
racing_color            = 0xFFFFFF
first_color             = 0xFF0000
second_color            = 0x00FF00
third_color             = 0x0000FF
finished_color          = 0xFFFFFF
race_changed            = False
race_event_loop         = None
use_coop                = False
coop_partner            = None
coop_opponent2          = None
coop_opponent1          = None
coop_source_name        = None
coop_label_source_name  = None
coop_text               = " "
coop_label_text         = "Race still in progress"

# ------------------------------------------------------------

def set_text():
    """takes scripted_text , sets its value in obs  """
    global race
    global full_name

    if not race:
        return

    if use_coop:
        set_coop_text()

    entrant = next((x for x in race.entrants if x.user.full_name == full_name), None)

    color = None
    time = "0:00:00.0"
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
    elif race.status.value == "finished":
        # race is finished and our user is not an entrant
        time = str(race.ended_at - race.started_at)[:9]
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

def set_coop_text():
    global coop_label_text
    global coop_text

    if race is None:
        return

    #coop_label_text = "Race still in progress"
    #coop_text = " "

    with source_ar(coop_source_name) as coop_source, data_ar() as settings:
        obs.obs_data_set_string(settings, "text", coop_text)
        obs.obs_source_update(coop_source, settings)
    
    with source_ar(coop_label_source_name) as coop_label_source, data_ar() as settings:
        obs.obs_data_set_string(settings, "text", coop_label_text)
        obs.obs_source_update(coop_label_source, settings)

def race_update_thread():
    global race_event_loop

    race_event_loop = asyncio.new_event_loop()
    race_event_loop.run_until_complete(race_updater())
    race_event_loop.run_forever()

def update_coop_text():
    global coop_label_text
    global coop_text



    entrant = next((x for x in race.entrants if x.user.full_name == full_name), None)
    partner = next((x for x in race.entrants if x.user.full_name == coop_partner), None)
    opponent1 = next((x for x in race.entrants if x.user.full_name == coop_opponent1), None)
    opponent2 = next((x for x in race.entrants if x.user.full_name == coop_opponent2), None)

    logger.debug(f"use_coop: {use_coop}")
    logger.debug(f"entrant name: {full_name}, entrant: {entrant}")
    logger.debug(f"entrant name: {coop_partner}, entrant: {partner}")
    logger.debug(f"entrant name: {coop_opponent1}, entrant: {opponent1}")
    logger.debug(f"entrant name: {coop_opponent2}, entrant: {opponent2}")

    if not use_coop or entrant is None or partner is None or opponent1 is None or opponent2 is None:
        return

    our_total = None
    opponent_total = None
    if entrant.finish_time and partner.finish_time:
        our_total = entrant.finish_time + partner.finish_time
        logger.info(f"calculated our average is {our_total / 2}")
    else:
        logger.info(f"we haven't finished yet")
    if opponent1.finish_time and opponent2.finish_time:
        opponent_total = opponent1.finish_time + opponent2.finish_time
        logger.info(f"calculated our opponent's average is {opponent_total / 2}")
    else:
        logger.info(f"our opponents haven't finished")
    if race.entrants_count_finished == 2:
        if our_total is not None:
            coop_label_text = "We won!"
            coop_text = str(our_total / 2)[:9]
        elif opponent_total is not None:
            coop_label_text = "They won. :("
            coop_text = str(opponent_total / 2)[:9]
    if race.entrants_count_finished == 3:
        current_timer = datetime.now(timezone.utc) - race.started_at
        time_to_beat = None
        if not entrant.finish_time:
            time_to_beat = opponent_total - partner.finish_time
            if time_to_beat < current_timer:
                coop_text = str(time_to_beat)[:9]
                coop_label_text = "I need to finish before"
            else:
                coop_label_text = "They won. :("
                opponent_avg = opponent_total / 2
                coop_text = str(opponent_avg)[:9]
        elif not partner.finish_time:
            time_to_beat = opponent_total - entrant.finish_time
            if time_to_beat < current_timer:
                coop_text = str(time_to_beat)[:9]
                coop_label_text = f"{partner.user.name} needs to finish before"
            else:
                coop_label_text = "Opponents won, average time:"
                opponent_avg = opponent_total / 2
                coop_label_text = str(opponent_avg)[:9]
        elif not opponent1.finish_time:
            time_to_beat = our_total - opponent2.finish_time
            if time_to_beat < current_timer:
                coop_text = str(time_to_beat)[:9]
                coop_label_text = f"{opponent1.user.name} needs to finish before"
            else:
                coop_label_text = "We won!!! Average time:"
                our_avg = our_total / 2
                coop_text = str(our_avg)[:9]
        elif not opponent2.finish_time:
            time_to_beat = our_total - opponent1.finish_time
            if time_to_beat < current_timer:
                coop_text = str(time_to_beat)[:9]
                coop_label_text = f"{opponent2.user.name} needs to finish before"
            else:
                coop_label_text = "We won!!! Average time:"
                our_avg = our_total / 2
                coop_text = str(our_avg)[:9]
    if race.entrants_count_finished == 4:
        our_total = entrant.finish_time + partner.finish_time
        opponent_total = opponent1.finish_time + opponent2.finish_time
        if our_total < opponent_total:
            coop_label_text = "We won!!! Average time:"
            our_avg = our_total / 2
            coop_text = str(our_avg)[:9]
        else:
            coop_label_text = "Opponents won, average time:"
            opponent_avg = opponent_total / 2
            coop_text = str(opponent_avg)[:9]

async def race_updater():
    global race
    global race_changed

    headers = {
        'User-Agent': "oro-obs-bot_alpha"
    }
    host = "racetime.gg"

    while True:
        if not check_race_updates:
            await asyncio.sleep(5.0)
        else:
            if race is None and selected_race != "":
                race = racetime_client.get_race(selected_race)
            if race is not None and race.websocket_url != "":
                async with websockets.connect("wss://racetime.gg" + race.websocket_url, host=host, extra_headers=headers) as ws:
                    logger.info(f"connected to websocket: {race.websocket_url}")
                    last_pong = datetime.now(timezone.utc)
                    race_changed = False
                    while True:
                        try:
                            if race_changed:
                                logger.info("new race selected")
                                race_changed = False
                                break
                            message = await asyncio.wait_for(ws.recv(), 5.0)
                            logger.info(f"received message from websocket: {message}")
                            data = json.loads(message)
                            if data.get("type") == "race.data":
                                r = race_from_dict(data.get("race"))
                                if r is not None and r.version > race.version:
                                    race = r
                                    update_coop_text()
                            elif data.get("type") == "pong":
                                last_pong = dateutil.parser.parse(data.get("date"))
                                pass
                        except asyncio.TimeoutError:
                            if datetime.now(timezone.utc) - last_pong > timedelta(seconds=20):
                                await ws.send(json.dumps({"action": "ping"}))
                        except websockets.ConnectionClosed:
                            logger.error(f"websocket connection closed")
                            race = None
                            break
        await asyncio.sleep(5.0)


def refresh_pressed(props, prop, *args, **kwargs):
    fill_source_list(obs.obs_properties_get(props, "source"))
    fill_race_list(obs.obs_properties_get(props, "race"), obs.obs_properties_get(props, "category_filter"))
    update_coop_text()
    return True

def new_race_selected(props, prop, settings):
    global race_changed
    global race
    global selected_race

    selected_race = obs.obs_data_get_string(settings, "race")
    r = racetime_client.get_race(selected_race)
    if r is not None:
        race = r
        update_coop_text()
        logger.info(f"new race selected: {race}")
        obs.obs_data_set_default_string(settings, "race_info", r.info)
        fill_coop_entrant_lists(props)
    else:
        obs.obs_data_set_default_string(settings, "race_info", "Race not found")
    
    race_changed = True
    return True

def new_category_selected(props, prop, settings):
    global category
    category = obs.obs_data_get_string(settings, "category_filter")
    logger.info(f"new category selected: {category}")
    fill_race_list(obs.obs_properties_get(props, "race"), prop)
    return True

def podium_toggled(props, prop, settings):
    vis = obs.obs_data_get_bool(settings, "use_podium")
    obs.obs_property_set_visible(obs.obs_properties_get(props, "podium_group"), vis)
    return True

def coop_toggled(props, prop, settings):
    vis = obs.obs_data_get_bool(settings, "use_coop")
    obs.obs_property_set_visible(obs.obs_properties_get(props, "coop_group"), vis)
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

# ------------------------------------------------------------

def script_description():
    return "<center><p>Select a text source to use as your timer and enter your full " + \
    "username on racetime.gg  (including discriminator). This only needs " + \
    "to be done once.\n\nThen select the race room each race you join and " + \
    "stop worrying about whether you started your timer or not.<hr/></p>"

def script_load(settings):
    global use_podium_colors
    use_podium_colors = obs.obs_data_get_bool(settings, "use_podium")

    race_update_t = Thread(target=race_update_thread)
    race_update_t.daemon = True
    race_update_t.start()

def script_save(settings):
    obs.obs_data_set_bool(settings, "use_podium", use_podium_colors)

def script_unload():
    global close_thread
    close_thread = True

def script_update(settings):
    global logger
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
    
    global use_coop
    global coop_partner
    global coop_opponent2
    global coop_opponent1
    global coop_source_name
    global coop_label_source_name

    obs.timer_remove(set_text)
    
    logger.disabled = not obs.obs_data_get_bool(settings, "enable_log")
    level = obs.obs_data_get_string(settings, "log_level")
    logger.handlers = []
    handler = logging.StreamHandler()
    if obs.obs_data_get_bool(settings, "log_to_file"):
        log_file = obs.obs_data_get_string(settings, "log_file")
        try:
            handler = logging.FileHandler(log_file)
        except:
            logger.error(f"Unable to open {log_file}")
    elif level == "Debug":
        handler.setLevel(logging.DEBUG)
    elif level == "Info":
        handler.setLevel(logging.INFO)
    else:
        handler.setLevel(logging.ERROR)

    handler.setFormatter(LogFormatter())
    logger.addHandler(handler)

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

    use_coop = obs.obs_data_get_bool(settings, "use_coop")
    coop_partner = obs.obs_data_get_string(settings, "coop_partner")
    coop_opponent1 = obs.obs_data_get_string(settings, "coop_opponent1")
    coop_opponent2 = obs.obs_data_get_string(settings, "coop_opponent2")
    coop_source_name = obs.obs_data_get_string(settings, "coop_source")
    coop_label_source_name = obs.obs_data_get_string(settings, "coop_label")

    if source_name != "" and selected_race != "":
        obs.timer_add(set_text, 100)
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
    obs.obs_property_list_add_string(category_list, "All", "All")

    obs.obs_property_list_add_string(race_list, "", "")
    races = racetime_client.get_races()
    if races is not None:
        categories = []
        for race in races:
            if category == "" or category == "All" or race.category.name == category:
                obs.obs_property_list_add_string(race_list, race.name, race.name)
            if not race.category.name in categories:
                categories.append(race.category.name)
                obs.obs_property_list_add_string(category_list, race.category.name, race.category.name)

def fill_coop_entrant_lists(props):
    fill_entrant_list(obs.obs_properties_get(props, "coop_partner"))
    fill_entrant_list(obs.obs_properties_get(props, "coop_opponent1"))
    fill_entrant_list(obs.obs_properties_get(props, "coop_opponent2"))


def fill_entrant_list(entrant_list):
    obs.obs_property_list_clear(entrant_list)
    obs.obs_property_list_add_string(entrant_list, "", "")
    if race is not None:
        for entrant in race.entrants:
            obs.obs_property_list_add_string(entrant_list, entrant.user.full_name, entrant.user.full_name)


def script_properties():
    props = obs.obs_properties_create()

    setup_group = obs.obs_properties_create()
    obs.obs_properties_add_group(props, "initial_setup", "Initial setup - Check to make changes", obs.OBS_GROUP_CHECKABLE, setup_group)
    p = obs.obs_properties_add_list(setup_group, "source", "Text Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    fill_source_list(p)
    obs.obs_properties_add_text(setup_group, "username", "Username", obs.OBS_TEXT_DEFAULT)
    logging = obs.obs_properties_add_bool(setup_group, "enable_log", "Enable logging")
    log_levels = obs.obs_properties_add_list(setup_group, "log_level", "Log lever", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_property_list_add_string(log_levels, "Error", "Error")
    obs.obs_property_list_add_string(log_levels, "Debug", "Debug")
    obs.obs_property_list_add_string(log_levels, "Info", "Info")
    obs.obs_property_set_long_description(logging, "Generally, only log errors unless you are developing or are trying to find a specific problem.")
    obs.obs_properties_add_bool(setup_group, "log_to_file", "Log to file?")
    #obs.obs_property_set_modified_callback(p, log_to_file_toggled)
    obs.obs_properties_add_path(setup_group, "log_file", "Log File", obs.OBS_PATH_FILE_SAVE, "Text files(*.txt)", None)

    category_list = obs.obs_properties_add_list(props, "category_filter", "Filter by Category", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    race_list = obs.obs_properties_add_list(props, "race", "Race", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
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

    p = obs.obs_properties_add_bool(props, "use_coop", "Display coop information?")
    obs.obs_property_set_modified_callback(p, coop_toggled)

    coop_group = obs.obs_properties_create()
    obs.obs_properties_add_group(props, "coop_group", "Co-op Mode", obs.OBS_GROUP_NORMAL, coop_group)
    obs.obs_property_set_visible(obs.obs_properties_get(props, "coop_group"), use_coop)
    p = obs.obs_properties_add_list(coop_group, "coop_partner", "Co-op Partner", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    p = obs.obs_properties_add_list(coop_group, "coop_opponent1", "Co-op Opponent 1", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    p = obs.obs_properties_add_list(coop_group, "coop_opponent2", "Co-op Opponent 2", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    fill_coop_entrant_lists(props)
    p = obs.obs_properties_add_list(coop_group, "coop_source", "Coop Text Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_property_set_long_description(p, "This text source will display the time that the last racer needs to finish for their team to win")
    fill_source_list(p)
    p = obs.obs_properties_add_list(coop_group, "coop_label", "Coop Label Text Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_property_set_long_description(p, "This text source will be use to display a label such as \'<PartnerName> needs to finish before\' based on who the last racer is")
    fill_source_list(p)

    return props
