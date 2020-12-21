import obspython as obs
from rtgg_obs import RacetimeObs
from scripting import fill_source_list


def script_update_setup_settings(settings, rtgg_obs: RacetimeObs):
    rtgg_obs.update_logger(
        obs.obs_data_get_bool(settings, "enable_log"),
        obs.obs_data_get_bool(settings, "log_to_file"),
        obs.obs_data_get_string(settings, "log_file"),
        obs.obs_data_get_string(settings, "log_level")
    )


def script_setup(props, new_race_selected, new_category_selected):
    setup_group = obs.obs_properties_create()
    obs.obs_properties_add_group(
        props, "initial_setup", "Initial setup - Check to make changes",
        obs.OBS_GROUP_CHECKABLE, setup_group
    )
    p = obs.obs_properties_add_list(
        setup_group, "source", "Text Source", obs.OBS_COMBO_TYPE_EDITABLE,
        obs.OBS_COMBO_FORMAT_STRING
    )
    fill_source_list(p)
    obs.obs_properties_add_text(
        setup_group, "username", "Username", obs.OBS_TEXT_DEFAULT)
    logging = obs.obs_properties_add_bool(
        setup_group, "enable_log", "Enable logging")
    log_levels = obs.obs_properties_add_list(
        setup_group, "log_level", "Log lever", obs.OBS_COMBO_TYPE_LIST,
        obs.OBS_COMBO_FORMAT_STRING
    )
    obs.obs_property_list_add_string(log_levels, "Error", "Error")
    obs.obs_property_list_add_string(log_levels, "Debug", "Debug")
    obs.obs_property_list_add_string(log_levels, "Info", "Info")
    obs.obs_property_set_long_description(
        logging, "Generally, only log errors unless you are developing or are "
        "trying to find a specific problem."
    )
    obs.obs_properties_add_bool(setup_group, "log_to_file", "Log to file?")
    category_list = obs.obs_properties_add_list(
        props, "category_filter", "Filter by Category",
        obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING
    )
    race_list = obs.obs_properties_add_list(
        props, "race", "Race",
        obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING
        )
    obs.obs_property_set_modified_callback(
        race_list, new_race_selected
    )
    obs.obs_property_set_modified_callback(
        category_list, new_category_selected)

    p = obs.obs_properties_add_text(
        props, "race_info", "Race Desc", obs.OBS_TEXT_MULTILINE)
    obs.obs_property_set_enabled(p, False)
