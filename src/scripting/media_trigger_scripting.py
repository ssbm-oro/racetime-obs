import gettext
import os

import obspython as obs
from rtgg_obs import RacetimeObs


def media_trigger_settings(props, rtgg_obs: RacetimeObs, index: int):
    lang = gettext.translation(
        "racetime-obs", localedir=os.environ['LOCALEDIR'])
    _ = lang.gettext

    media_player_group = obs.obs_properties_create()
    name = f"media_trigger_#{index}"
    obs.obs_properties_add_group(
            props, name, _("Media Trigger #") + f"{index}",
            obs.OBS_GROUP_NORMAL, media_player_group
        )
    obs.obs_property_set_visible(
        obs.obs_properties_get(props, "media_player_group"),
        rtgg_obs.media_player.enabled
    )
    obs.obs_properties_add_path(
        media_player_group, f"media_path_#{index}",
        _("Sound File"), obs.OBS_PATH_FILE,
        "Audio Files (*.mp3 *.aac *.wav *.wma)", None
    )
    p = obs.obs_properties_add_list(
        media_player_group, f"trigger_type_#{index}", _("Type of Trigger"),
        obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_property_list_add_string(p, "", "")
    obs.obs_property_list_add_string(p, _("Chat"), "chat")
    obs.obs_property_list_add_string(p, _("Finish Place"), "finish")
    obs.obs_property_list_add_string(p, _("Timer"), "time")
    obs.obs_property_set_modified_callback(p, media_type_changed)
    p = obs.obs_properties_add_list(
        media_player_group, f"monitoring_type_#{index}", _("Monitoring Type"),
        obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_INT)
    obs.obs_property_list_add_int(
        p, _("Only Listen"), obs.OBS_MONITORING_TYPE_MONITOR_ONLY)
    obs.obs_property_list_add_int(
        p, _("Only Stream"), obs.OBS_MONITORING_TYPE_NONE)
    obs.obs_property_list_add_int(
        p, _("Listen and Stream"), obs.OBS_MONITORING_TYPE_MONITOR_AND_OUTPUT)


def media_type_changed(props, prop, settings):
    pass


def chat_media_trigger_settings(props, index: int):
    lang = gettext.translation(
        "racetime-obs", localedir=os.environ['LOCALEDIR'])
    _ = lang.gettext

    obs.obs_properties_add_bool(props, f"trigger_chat_bot_#{index}", _("Bot?"))
    obs.obs_properties_add_bool(
        props, f"trigger_chat_highlight_#{index}", _("Highlighted?"))
    obs.obs_properties_add_bool(
        props, f"trigger_chat_system_#{index}", _("System?"))


def finish_media_trigger_settings(props, index: int):
    """
    Settings for a media trigger based on what place the entrant finishes
    """
    lang = gettext.translation(
        "racetime-obs", localedir=os.environ['LOCALEDIR'])
    _ = lang.gettext

    obs.obs_properties_add_int(
        props, f"trigger_finish_place_#{index}", _("Finish Place <="),
        1, 10, 1)
    obs.obs_properties_add_int(
        props, f"trigger_finish_entrants_#{index}", _("Num. Entrants >="),
        2, 255, 1)


def timer_media_trigger_settings(props, index: int):
    lang = gettext.translation(
        "racetime-obs", localedir=os.environ['LOCALEDIR'])
    _ = lang.gettext

    obs.obs_properties_add_float_slider(
        props, f"trigger_timer_time_#{index}", _("Start playing at "),
        -15.0, 60, 0.1)
