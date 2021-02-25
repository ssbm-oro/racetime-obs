import gettext

import os

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
    rtgg_obs.preview_mode = obs.obs_data_get_bool(settings, "preview_mode")


def script_setup(props, new_race_selected, new_category_selected):
    lang = gettext.translation(
        "racetime-obs", localedir=os.environ['LOCALEDIR'])
    _ = lang.gettext

    setup_group = obs.obs_properties_create()
    obs.obs_properties_add_group(
        props, "initial_setup", _("Initial setup - Check to make changes"),
        obs.OBS_GROUP_CHECKABLE, setup_group
    )
    p = obs.obs_properties_add_list(
        setup_group, "source", _("Text Source"), obs.OBS_COMBO_TYPE_EDITABLE,
        obs.OBS_COMBO_FORMAT_STRING
    )
    fill_source_list(p)
    obs.obs_properties_add_text(
        setup_group, "username", _("Username"), obs.OBS_TEXT_DEFAULT)
    logging = obs.obs_properties_add_bool(
        setup_group, "enable_log", _("Enable logging"))
    log_levels = obs.obs_properties_add_list(
        setup_group, "log_level", _("Log level"), obs.OBS_COMBO_TYPE_LIST,
        obs.OBS_COMBO_FORMAT_STRING
    )
    obs.obs_property_list_add_string(log_levels, _("Error"), "error")
    obs.obs_property_list_add_string(log_levels, _("Debug"), "debug")
    obs.obs_property_list_add_string(log_levels, _("Info"), "info")
    obs.obs_property_set_long_description(
        logging, _(
            "Generally, only log errors unless you are developing or are "
            "trying to find a specific problem.")
    )
    obs.obs_properties_add_bool(setup_group, "log_to_file", _("Log to file?"))
    obs.obs_properties_add_path(
        setup_group, "log_file", _("Log File"), obs.OBS_PATH_FILE_SAVE, "*",
        None
    )

    preview = obs.obs_properties_add_bool(
        setup_group, "preview_mode", "Preview Mode")
    obs.obs_property_set_long_description(
        preview, "Puts preview values in "
        "each component's text source to help arrange up your layout.")

    category_list = obs.obs_properties_add_list(
        props, "category_filter", _("Filter by Category"),
        obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING
    )
    race_list = obs.obs_properties_add_list(
        props, "race", _("Race"),
        obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING
        )
    obs.obs_property_set_modified_callback(
        race_list, new_race_selected
    )
    obs.obs_property_set_modified_callback(
        category_list, new_category_selected)

    p = obs.obs_properties_add_text(
        props, "race_info", _("Race Desc"), obs.OBS_TEXT_MULTILINE)
    obs.obs_property_set_enabled(p, False)
