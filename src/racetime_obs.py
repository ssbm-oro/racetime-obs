from threading import Thread
import obspython as obs
import racetime_client
from rtgg_obs import RacetimeObs

rtgg_obs = RacetimeObs()

def script_description():
    return "<center><p>Select a text source to use as your timer and enter your full " + \
        "username on racetime.gg  (including discriminator). This only needs " + \
        "to be done once.\n\nThen select the race room each race you join and " + \
        "stop worrying about whether you started your timer or not.<hr/></p>"


def script_load(settings):
    rtgg_obs.timer.use_podium_colors = obs.obs_data_get_bool(settings, "use_podium")

    race_update_t = Thread(target=rtgg_obs.race_update_thread)
    race_update_t.daemon = True
    race_update_t.start()


def script_save(settings):
    obs.obs_data_set_bool(settings, "use_podium", rtgg_obs.timer.use_podium_colors)

def script_update(settings):

    obs.timer_remove(rtgg_obs.update_sources)

    rtgg_obs.update_logger(obs.obs_data_get_bool(settings, "enable_log"),
        obs.obs_data_get_bool(settings, "log_to_file"),
        obs.obs_data_get_string(settings, "log_file"), 
        obs.obs_data_get_string(settings, "log_level"))

    rtgg_obs.full_name = obs.obs_data_get_string(settings, "username")

    rtgg_obs.timer.source_name = obs.obs_data_get_string(settings, "source")

    rtgg_obs.selected_race = obs.obs_data_get_string(settings, "race")
    rtgg_obs.category = obs.obs_data_get_string(settings, "category_filter")

    rtgg_obs.timer.use_podium_colors = obs.obs_data_get_bool(settings, "use_podium")
    rtgg_obs.timer.pre_color = obs.obs_data_get_int(settings, "pre_color")
    rtgg_obs.timer.first_color = obs.obs_data_get_int(settings, "first_color")
    rtgg_obs.timer.second_color = obs.obs_data_get_int(settings, "second_color")
    rtgg_obs.timer.third_color = obs.obs_data_get_int(settings, "third_color")
    rtgg_obs.timer.racing_color = obs.obs_data_get_int(settings, "racing_color")
    rtgg_obs.timer.finished_color = obs.obs_data_get_int(settings, "finished_color")

    if rtgg_obs.timer.source_name != "" and rtgg_obs.selected_race != "":
        obs.timer_add(rtgg_obs.update_sources, 100)
        rtgg_obs.timer.enabled = True
    else:
        rtgg_obs.timer.enabled = False
    rtgg_obs.logger.debug(f"timer.enabled is {rtgg_obs.timer.enabled}")
    rtgg_obs.logger.debug(f"timer.source_name is {rtgg_obs.timer.source_name}")
    rtgg_obs.logger.debug(f"selected_race is {rtgg_obs.selected_race}")

    rtgg_obs.coop.enabled = obs.obs_data_get_bool(settings, "use_coop")
    rtgg_obs.coop.partner = obs.obs_data_get_string(settings, "coop_partner")
    rtgg_obs.coop.opponent1 = obs.obs_data_get_string(settings, "coop_opponent1")
    rtgg_obs.coop.opponent2 = obs.obs_data_get_string(settings, "coop_opponent2")
    rtgg_obs.coop.source_name = obs.obs_data_get_string(settings, "coop_source")
    rtgg_obs.coop.label_source_name = obs.obs_data_get_string(settings, "coop_label")

    rtgg_obs.qualifier.enabled = obs.obs_data_get_bool(settings, "use_qualifier")
    rtgg_obs.qualifier.qualifier_cutoff = obs.obs_data_get_int(settings, "qualifier_cutoff")
    rtgg_obs.qualifier.qualifier_par_source = obs.obs_data_get_string(
        settings, "qualifier_par_source")
    rtgg_obs.qualifier.qualifier_score_source = obs.obs_data_get_string(
        settings, "qualifier_score_source")


def script_defaults(settings):
    obs.obs_data_set_default_string(settings, "race_info", "Race info")
    obs.obs_data_set_default_string(settings, "race", "")

def script_properties():
    props = obs.obs_properties_create()

    setup_group = obs.obs_properties_create()
    obs.obs_properties_add_group(
        props, "initial_setup", "Initial setup - Check to make changes", obs.OBS_GROUP_CHECKABLE, setup_group)
    p = obs.obs_properties_add_list(
        setup_group, "source", "Text Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    rtgg_obs.fill_source_list(p)
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
        props, "podium_group"), rtgg_obs.timer.use_podium_colors)

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
        obs.obs_properties_get(props, "coop_group"), rtgg_obs.coop.enabled)
    p = obs.obs_properties_add_list(
        coop_group, "coop_partner", "Co-op Partner", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    p = obs.obs_properties_add_list(
        coop_group, "coop_opponent1", "Co-op Opponent 1", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    p = obs.obs_properties_add_list(
        coop_group, "coop_opponent2", "Co-op Opponent 2", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    rtgg_obs.fill_coop_entrant_lists(props)
    p = obs.obs_properties_add_list(coop_group, "coop_source", "Coop Text Source",
                                    obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_property_set_long_description(
        p, "This text source will display the time that the last racer needs to finish for their team to win")
    rtgg_obs.fill_source_list(p)
    p = obs.obs_properties_add_list(coop_group, "coop_label", "Coop Label Text Source",
                                    obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_property_set_long_description(
        p, "This text source will be use to display a label such as \'<PartnerName> needs to finish before\' based on who the last racer is")
    rtgg_obs.fill_source_list(p)

    p = obs.obs_properties_add_bool(
        props, "use_qualifier", "Display race results as tournament qualifier?")
    obs.obs_property_set_modified_callback(p, qualifier_toggled)

    qualifier_group = obs.obs_properties_create()
    obs.obs_properties_add_group(
        props, "qualifier_group", "Qualifier Mode", obs.OBS_GROUP_NORMAL, qualifier_group)
    obs.obs_property_set_visible(
        obs.obs_properties_get(props, "qualifier_group"), rtgg_obs.qualifier.enabled)
    p = obs.obs_properties_add_int_slider(
        qualifier_group, "qualifier_cutoff", "Use Top X as par time, where X=", 3, 10, 1)
    p = obs.obs_properties_add_list(qualifier_group, "qualifier_par_source",
                                    "Qualifier Par Time Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    rtgg_obs.fill_source_list(p)
    p = obs.obs_properties_add_list(qualifier_group, "qualifier_score_source",
                                    "Qualifier Score Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    rtgg_obs.fill_source_list(p)

    return props

def refresh_pressed(props, prop, *args, **kwargs):
    rtgg_obs.fill_source_list(obs.obs_properties_get(props, "source"))
    rtgg_obs.fill_source_list(obs.obs_properties_get(props, "coop_label"))
    rtgg_obs.fill_source_list(obs.obs_properties_get(props, "coop_text"))
    rtgg_obs.fill_source_list(obs.obs_properties_get(props, "qualifier_par_source"))
    rtgg_obs.fill_source_list(obs.obs_properties_get(props, "qualifier_score_source"))
    rtgg_obs.fill_race_list(obs.obs_properties_get(props, "race"),
                obs.obs_properties_get(props, "category_filter"))
    if rtgg_obs.race is not None:
        rtgg_obs.coop.update_coop_text(rtgg_obs.race, rtgg_obs.full_name)
        rtgg_obs.qualifier.update_qualifier_text(rtgg_obs.race, rtgg_obs.full_name)
    return True


def new_race_selected(props, prop, settings):
    rtgg_obs.selected_race = obs.obs_data_get_string(settings, "race")
    r = racetime_client.get_race(rtgg_obs.selected_race)
    if r is not None:
        rtgg_obs.race = r
        rtgg_obs.coop.update_coop_text(rtgg_obs.race, rtgg_obs.full_name)
        rtgg_obs.qualifier.update_qualifier_text(rtgg_obs.race, rtgg_obs.full_name)
        rtgg_obs.logger.info(f"new race selected: {rtgg_obs.race}")
        obs.obs_data_set_default_string(settings, "race_info", r.info)
        rtgg_obs.fill_coop_entrant_lists(props)
    else:
        obs.obs_data_set_default_string(
            settings, "race_info", "Race not found")

    rtgg_obs.race_changed = True
    return True


def new_category_selected(props, prop, settings):
    rtgg_obs.category = obs.obs_data_get_string(settings, "category_filter")
    rtgg_obs.logger.info(f"new category selected: {rtgg_obs.category}")
    rtgg_obs.fill_race_list(obs.obs_properties_get(props, "race"), prop)
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
