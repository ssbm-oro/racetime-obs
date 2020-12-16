import json
import websockets
from websockets.client import WebSocketClientProtocol
import obspython as obs
from datetime import datetime, timedelta, timezone
import racetime_client
from models.race import Entrant, Race, race_from_dict
import asyncio
from threading import Thread
import websockets
import dateutil
import logging
from helpers.LogFormatter import LogFormatter
from helpers.obs_context_manager import source_ar, source_list_ar, data_ar

# ------------------------------------------------------------

logger = logging.Logger("racetime-obs")
source_name = ""
timer_text = ""
full_name = ""
category = ""
race: Race = None
selected_race = ""
check_race_updates = False
use_podium_colors = False
pre_color = 0xFFFFFF
racing_color = 0xFFFFFF
first_color = 0xFF0000
second_color = 0x00FF00
third_color = 0x0000FF
finished_color = 0xFFFFFF
race_changed = False
use_coop = False
coop_partner = None
coop_opponent2 = None
coop_opponent1 = None
coop_source_name = None
coop_label_source_name = None
coop_text = " "
coop_label_text = "Race still in progress"
use_qualifier = False
qualifier_cutoff = 3
qualifier_par_source = ""
qualifier_score_source = ""
qualifier_par_text = " "
entrant_score = " "

# ------------------------------------------------------------


def set_timer_text():
    global race
    global full_name

    if not race:
        return
    if use_coop:
        set_coop_text()
    if use_qualifier:
        set_qualifier_text()

    color, time = get_timer_text(race, full_name)
    with source_ar(source_name) as source, data_ar() as settings:
        obs.obs_data_set_string(settings, "text", time)
        if use_podium_colors:
            set_color(source, settings, color)
        obs.obs_source_update(source, settings)


def get_timer_text(race: Race, full_name: str):
    entrant = race.get_entrant_by_name(full_name)
    color = racing_color
    time = "--:--:--.-"
    if race.status.value == "open" or race.status.value == "invitational":
        time = timer_to_str(race.start_delay)
        color = pre_color
    elif entrant is not None:
        if entrant.finish_time is not None:
            time = timer_to_str(entrant.finish_time)
            color = get_color(entrant.place)
        elif entrant.status.value == "dnf" or entrant.status.value == "dq" or race.status.value == "cancelled":
            color = 0xFF0000
        elif race.started_at is not None:
            timer = datetime.now(timezone.utc) - race.started_at
            time = timer_to_str(timer)
    elif race.status.value == "finished":
        # race is finished and our user is not an entrant
        time = timer_to_str(race.ended_at - race.started_at)
    elif race.started_at is not None:
        timer = datetime.now(timezone.utc) - race.started_at
        time = timer_to_str(timer)
    else:
        return
    return color, time


def get_color(place: int) -> int:
    if place == 1:
        return first_color
    elif place == 2:
        return second_color
    elif place == 3:
        return third_color
    else:
        return finished_color


def timer_to_str(timer: timedelta) -> str:
    if timer.total_seconds() < 0.0:
        return "-0:00:{:04.1f}".format(timer.total_seconds() * -1.0)
    else:
        return str(timer)[:9]


def set_coop_text():
    global coop_label_text
    global coop_text

    if race is None:
        return

    with source_ar(coop_source_name) as coop_source, data_ar() as settings:
        obs.obs_data_set_string(settings, "text", coop_text)
        obs.obs_source_update(coop_source, settings)

    with source_ar(coop_label_source_name) as coop_label_source, data_ar() as settings:
        obs.obs_data_set_string(settings, "text", coop_label_text)
        obs.obs_source_update(coop_label_source, settings)


def set_qualifier_text():
    global qualifier_par_text
    global entrant_score

    if race is None:
        return

    with source_ar(qualifier_par_source) as par_source, data_ar() as settings:
        obs.obs_data_set_string(settings, "text", qualifier_par_text)
        obs.obs_source_update(par_source, settings)

    with source_ar(qualifier_score_source) as score_source, data_ar() as settings:
        obs.obs_data_set_string(settings, "text", entrant_score)
        obs.obs_source_update(score_source, settings)


def update_coop_text(race: Race):
    global coop_label_text
    global coop_text

    if not race:
        return

    entrant = race.get_entrant_by_name(full_name)
    partner = race.get_entrant_by_name(coop_partner)
    opponent1 = race.get_entrant_by_name(coop_opponent1)
    opponent2 = race.get_entrant_by_name(coop_opponent2)

    if not use_coop or entrant is None or partner is None or opponent1 is None or opponent2 is None:
        return

    logger.debug(f"use_coop: {use_coop}")
    logger.debug(f"entrant name: {full_name}, entrant: {entrant}")
    logger.debug(f"entrant name: {coop_partner}, entrant: {partner}")
    logger.debug(f"entrant name: {coop_opponent1}, entrant: {opponent1}")
    logger.debug(f"entrant name: {coop_opponent2}, entrant: {opponent2}")

    our_total, opponent_total = get_coop_times(
        entrant, partner, opponent1, opponent2)
    if race.entrants_count_finished == 2:
        if our_total is not None:
            coop_label_text = "We won!"
            coop_text = timer_to_str(our_total / 2)
        elif opponent_total is not None:
            coop_label_text = "They won. :("
            coop_text = timer_to_str(opponent_total / 2)
    if race.entrants_count_finished == 3:
        current_timer = datetime.now(timezone.utc) - race.started_at
        time_to_beat = None
        if not entrant.finish_time:
            coop_label_text, coop_text = get_coop_text(
                "I need ", partner, opponent_total, current_timer)
        elif not partner.finish_time:
            prefix = partner.user.name + " needs to finish before"
            coop_label_text, coop_text = get_coop_text(
                prefix, entrant, opponent1, opponent2, current_timer)
        elif not opponent1.finish_time:
            prefix = opponent1.user.name + " needs "
            coop_label_text, coop_text = get_coop_text(
                prefix, opponent2, entrant, partner, current_timer)
        elif not opponent2.finish_time:
            prefix = opponent2.user.name + " needs "
            coop_label_text, coop_text = get_coop_text(
                prefix, opponent1, entrant, partner, current_timer)
    if race.entrants_count_finished == 4:
        our_total = entrant.finish_time + partner.finish_time
        opponent_total = opponent1.finish_time + opponent2.finish_time
        if our_total < opponent_total:
            coop_label_text = "We won!!! Average time:"
            coop_text = timer_to_str(our_total / 2)
        else:
            coop_label_text = "Opponents won, average time:"
            coop_text = timer_to_str(opponent_total / 2)


def get_coop_text(label_text_start: str, finished_partner: Entrant, finished1: Entrant, finished2: Entrant, current_timer: timedelta):
    finished_team_total = finished1.finish_time + finished2.finish_time
    time_to_beat = finished_team_total - finished_partner.finish_time
    if time_to_beat < current_timer:
        coop_text = timer_to_str(time_to_beat)
        coop_label_text = label_text_start + "to finish before"
    else:
        coop_label_text = finished1.user.name + finished2.user.name + " won"
        coop_text = timer_to_str(finished_team_total / 2)
    return coop_label_text, coop_text


def get_coop_times(entrant, partner, opponent1, opponent2):
    our_total = None
    opponent_total = None
    if entrant.finish_time and partner.finish_time:
        our_total = entrant.finish_time + partner.finish_time
        logger.debug(f"calculated our average is {our_total / 2}")
    else:
        logger.debug(f"we haven't finished yet")
    if opponent1.finish_time and opponent2.finish_time:
        opponent_total = opponent1.finish_time + opponent2.finish_time
        logger.debug(
            f"calculated our opponent's average is {opponent_total / 2}")
    else:
        logger.debug(f"our opponents haven't finished")
    return our_total, opponent_total


def update_qualifier_text(race: Race):
    global qualifier_par_text
    global entrant_score
    if not use_qualifier or race is None:
        return

    entrant = race.get_entrant_by_name(full_name)
    logger.debug(entrant)

    qualifier_par_text = " "
    entrant_score = " "
    if race.entrants_count_finished >= qualifier_cutoff:
        par_time = timedelta(microseconds=0)
        for i in range(1, qualifier_cutoff + 1):
            if race.get_entrant_by_place(i).finish_time is None:
                logger.error("error: qualifier finish time is None")
                return
            logger.debug(
                f"finish time for rank {i} is {race.get_entrant_by_place(i).finish_time}")
            par_time += race.get_entrant_by_place(i).finish_time
        par_time = par_time / qualifier_cutoff
        logger.debug(par_time)
        qualifier_par_text = timer_to_str(par_time)

        if entrant and entrant.finish_time is not None:
            entrant_score = str(2 - (entrant.finish_time / par_time))[:4]
        logger.debug(entrant_score)


def race_update_thread():
    race_event_loop = asyncio.new_event_loop()
    race_event_loop.run_until_complete(race_updater())
    race_event_loop.run_forever()


async def race_updater():
    global race
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
                    logger.info(
                        f"connected to websocket: {race.websocket_url}")
                    await process_messages(ws)
        await asyncio.sleep(5.0)


async def process_messages(ws: WebSocketClientProtocol):
    global race
    global race_changed

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
            last_pong = process_ws_message(data, last_pong)
        except asyncio.TimeoutError:
            if datetime.now(timezone.utc) - last_pong > timedelta(seconds=20):
                await ws.send(json.dumps({"action": "ping"}))
        except websockets.ConnectionClosed:
            logger.error(f"websocket connection closed")
            race = None
            break


def process_ws_message(data, last_pong):
    global race
    if data.get("type") == "race.data":
        r = race_from_dict(data.get("race"))
        if r is not None and r.version > race.version:
            race = r
            update_coop_text(race)
            update_qualifier_text(race)
    elif data.get("type") == "pong":
        last_pong = dateutil.parser.parse(data.get("date"))
        pass
    return last_pong


def refresh_pressed(props, prop, *args, **kwargs):
    fill_source_list(obs.obs_properties_get(props, "source"))
    fill_source_list(obs.obs_properties_get(props, "coop_text"))
    fill_source_list(obs.obs_properties_get(props, "coop_label"))
    fill_source_list(obs.obs_properties_get(props, "qualifier_par_source"))
    fill_source_list(obs.obs_properties_get(props, "qualifier_score_source"))
    fill_race_list(obs.obs_properties_get(props, "race"),
                   obs.obs_properties_get(props, "category_filter"))
    update_coop_text(race)
    update_qualifier_text(race)
    return True


def new_race_selected(props, prop, settings):
    global race_changed
    global race
    global selected_race

    selected_race = obs.obs_data_get_string(settings, "race")
    r = racetime_client.get_race(selected_race)
    if r is not None:
        race = r
        update_coop_text(race)
        update_qualifier_text(race)
        logger.info(f"new race selected: {race}")
        obs.obs_data_set_default_string(settings, "race_info", r.info)
        fill_coop_entrant_lists(props)
    else:
        obs.obs_data_set_default_string(
            settings, "race_info", "Race not found")

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
    obs.obs_property_set_visible(
        obs.obs_properties_get(props, "podium_group"), vis)
    return True


def coop_toggled(props, prop, settings):
    vis = obs.obs_data_get_bool(settings, "use_coop")
    obs.obs_property_set_visible(
        obs.obs_properties_get(props, "coop_group"), vis)
    return True


def qualifier_toggled(props, prop, settings):
    vis = obs.obs_data_get_bool(settings, "use_qualifier")
    obs.obs_property_set_visible(
        obs.obs_properties_get(props, "qualifier_group"), vis)
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

    global use_qualifier
    global qualifier_cutoff
    global qualifier_par_source
    global qualifier_score_source

    obs.timer_remove(set_timer_text)

    logger.disabled = not obs.obs_data_get_bool(settings, "enable_log")
    level = obs.obs_data_get_string(settings, "log_level")
    update_logger(obs.obs_data_get_bool(settings, "log_to_file"),
                  obs.obs_data_get_string(settings, "log_file"), level)

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
        obs.timer_add(set_timer_text, 100)
        check_race_updates = True
    else:
        check_race_updates = False

    full_name = obs.obs_data_get_string(settings, "username")

    use_qualifier = obs.obs_data_get_bool(settings, "use_qualifier")
    qualifier_cutoff = obs.obs_data_get_int(settings, "qualifier_cutoff")
    qualifier_par_source = obs.obs_data_get_string(
        settings, "qualifier_par_source")
    qualifier_score_source = obs.obs_data_get_string(
        settings, "qualifier_score_source")


def update_logger(log_to_file: bool, log_file: str, level: str):
    logger.handlers = []
    handler = logging.StreamHandler()
    if log_to_file:
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
                obs.obs_property_list_add_string(
                    race_list, race.name, race.name)
            if not race.category.name in categories:
                categories.append(race.category.name)
                obs.obs_property_list_add_string(
                    category_list, race.category.name, race.category.name)


def fill_coop_entrant_lists(props):
    fill_entrant_list(obs.obs_properties_get(props, "coop_partner"))
    fill_entrant_list(obs.obs_properties_get(props, "coop_opponent1"))
    fill_entrant_list(obs.obs_properties_get(props, "coop_opponent2"))


def fill_entrant_list(entrant_list):
    obs.obs_property_list_clear(entrant_list)
    obs.obs_property_list_add_string(entrant_list, "", "")
    if race is not None:
        for entrant in race.entrants:
            obs.obs_property_list_add_string(
                entrant_list, entrant.user.full_name, entrant.user.full_name)


def script_properties():
    props = obs.obs_properties_create()

    setup_group = obs.obs_properties_create()
    obs.obs_properties_add_group(
        props, "initial_setup", "Initial setup - Check to make changes", obs.OBS_GROUP_CHECKABLE, setup_group)
    p = obs.obs_properties_add_list(
        setup_group, "source", "Text Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    fill_source_list(p)
    obs.obs_properties_add_text(
        setup_group, "username", "Username", obs.OBS_TEXT_DEFAULT)
    logging = obs.obs_properties_add_bool(
        setup_group, "enable_log", "Enable logging")
    log_levels = obs.obs_properties_add_list(
        setup_group, "log_level", "Log lever", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_property_list_add_string(log_levels, "Error", "Error")
    obs.obs_property_list_add_string(log_levels, "Debug", "Debug")
    obs.obs_property_list_add_string(log_levels, "Info", "Info")
    obs.obs_property_set_long_description(
        logging, "Generally, only log errors unless you are developing or are trying to find a specific problem.")
    obs.obs_properties_add_bool(setup_group, "log_to_file", "Log to file?")
    #obs.obs_property_set_modified_callback(p, log_to_file_toggled)
    obs.obs_properties_add_path(
        setup_group, "log_file", "Log File", obs.OBS_PATH_FILE_SAVE, "Text files(*.txt)", None)

    category_list = obs.obs_properties_add_list(
        props, "category_filter", "Filter by Category", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    race_list = obs.obs_properties_add_list(
        props, "race", "Race", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_property_set_modified_callback(race_list, new_race_selected)
    obs.obs_property_set_modified_callback(
        category_list, new_category_selected)

    p = obs.obs_properties_add_text(
        props, "race_info", "Race Desc", obs.OBS_TEXT_MULTILINE)
    obs.obs_property_set_enabled(p, False)

    refresh = obs.obs_properties_add_button(
        props, "button", "Refresh", lambda *props: None)
    obs.obs_property_set_modified_callback(refresh, refresh_pressed)

    p = obs.obs_properties_add_bool(
        props, "use_podium", "Use custom color for podium finishes?")
    obs.obs_property_set_modified_callback(p, podium_toggled)

    podium_group = obs.obs_properties_create()
    obs.obs_properties_add_group(
        props, "podium_group", "Podium Colors", obs.OBS_GROUP_NORMAL, podium_group)
    obs.obs_property_set_visible(obs.obs_properties_get(
        props, "podium_group"), use_podium_colors)

    obs.obs_properties_add_color(podium_group, "pre_color", "Pre-race:")
    obs.obs_properties_add_color(podium_group, "racing_color", "Still racing:")
    obs.obs_properties_add_color(podium_group, "first_color", "1st place:")
    obs.obs_properties_add_color(podium_group, "second_color", "2nd place:")
    obs.obs_properties_add_color(podium_group, "third_color", "3rd place:")
    obs.obs_properties_add_color(
        podium_group, "finished_color", "After podium:")

    p = obs.obs_properties_add_bool(
        props, "use_coop", "Display coop information?")
    obs.obs_property_set_modified_callback(p, coop_toggled)

    coop_group = obs.obs_properties_create()
    obs.obs_properties_add_group(
        props, "coop_group", "Co-op Mode", obs.OBS_GROUP_NORMAL, coop_group)
    obs.obs_property_set_visible(
        obs.obs_properties_get(props, "coop_group"), use_coop)
    p = obs.obs_properties_add_list(
        coop_group, "coop_partner", "Co-op Partner", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    p = obs.obs_properties_add_list(
        coop_group, "coop_opponent1", "Co-op Opponent 1", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    p = obs.obs_properties_add_list(
        coop_group, "coop_opponent2", "Co-op Opponent 2", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    fill_coop_entrant_lists(props)
    p = obs.obs_properties_add_list(coop_group, "coop_source", "Coop Text Source",
                                    obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_property_set_long_description(
        p, "This text source will display the time that the last racer needs to finish for their team to win")
    fill_source_list(p)
    p = obs.obs_properties_add_list(coop_group, "coop_label", "Coop Label Text Source",
                                    obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_property_set_long_description(
        p, "This text source will be use to display a label such as \'<PartnerName> needs to finish before\' based on who the last racer is")
    fill_source_list(p)

    p = obs.obs_properties_add_bool(
        props, "use_qualifier", "Display race results as tournament qualifier?")
    obs.obs_property_set_modified_callback(p, qualifier_toggled)

    qualifier_group = obs.obs_properties_create()
    obs.obs_properties_add_group(
        props, "qualifier_group", "Qualifier Mode", obs.OBS_GROUP_NORMAL, qualifier_group)
    p = obs.obs_properties_add_int_slider(
        qualifier_group, "qualifier_cutoff", "Use Top X as par time, where X=", 3, 10, 1)
    p = obs.obs_properties_add_list(qualifier_group, "qualifier_par_source",
                                    "Qualifier Par Time Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    fill_source_list(p)
    p = obs.obs_properties_add_list(qualifier_group, "qualifier_score_source",
                                    "Qualifier Score Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    fill_source_list(p)

    return props
