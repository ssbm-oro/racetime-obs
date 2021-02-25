import gettext
import os

from helpers.obs_context_manager import media_source_ar
import obspython as obs
from rtgg_obs import RacetimeObs

_ = gettext.gettext


def script_update_media_player_settings(settings, rtgg_obs: RacetimeObs):
    rtgg_obs.media_player.play_media_callback = play_sound
    rtgg_obs.media_player.enabled = obs.obs_data_get_bool(
        settings, "use_media_player")
    rtgg_obs.media_player.monitoring_type = obs.obs_data_get_int(
        settings, "monitoring_type")
    rtgg_obs.media_player.ping_chat_messages = obs.obs_data_get_bool(
        settings, "use_chat_pings")
    rtgg_obs.media_player.chat_media_file = obs.obs_data_get_string(
        settings, "chat_ping_sound")
    first_place_sound = obs.obs_data_get_string(settings,
                                                "first_place_sound")
    if first_place_sound is not None and first_place_sound != "":
        rtgg_obs.media_player.remove_trigger(0)
        rtgg_obs.media_player.add_trigger(first_place_sound, place_trigger=1)
        rtgg_obs.media_player.play_media_callback = play_sound


def script_media_player_settings(
    props, rtgg_obs: RacetimeObs, media_player_toggled
):
    lang = gettext.translation(
        "racetime-obs", localedir=os.environ['LOCALEDIR'])
    _ = lang.gettext

    p = obs.obs_properties_add_bool(
        props, "use_media_player", _("Enable sounds?")
    )
    obs.obs_property_set_modified_callback(p, media_player_toggled)
    media_player_group = obs.obs_properties_create()
    obs.obs_properties_add_group(
            props, "media_player_group", _("Media Player Mode"),
            obs.OBS_GROUP_NORMAL, media_player_group
        )
    obs.obs_property_set_visible(
        obs.obs_properties_get(props, "media_player_group"),
        rtgg_obs.media_player.enabled
    )
    monitoring_list = obs.obs_properties_add_list(
        media_player_group, "monitoring_type", _("Monitoring Type"),
        obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_INT)
    obs.obs_property_list_add_int(
        monitoring_list, _("Listen Only"),
        obs.OBS_MONITORING_TYPE_MONITOR_ONLY
    )
    obs.obs_property_list_add_int(
        monitoring_list, _("Stream Only"), obs.OBS_MONITORING_TYPE_NONE)
    obs.obs_property_list_add_int(
        monitoring_list, _("Listen and Stream"),
        obs.OBS_MONITORING_TYPE_MONITOR_AND_OUTPUT)
    p = obs.obs_properties_add_bool(
        media_player_group, "use_chat_pings", _("Chat Pings"))
    obs.obs_property_set_long_description(
        p, _("Enable this and set choose a sound file to play when a bot posts"
             " or when someone @s you in racetime.gg chat")
    )
    p = obs.obs_properties_add_path(
        media_player_group, "chat_ping_sound",
        _("Chat media file"), obs.OBS_PATH_FILE,
        "Audio Files (*.mp3 *.aac *.wav *.wma)", None
    )
    obs.obs_properties_add_path(
        media_player_group, "first_place_sound",
        _("First Place Sound"), obs.OBS_PATH_FILE,
        "Audio Files (*.mp3 *.aac *.wav *.wma)", None
    )
    obs.obs_property_set_long_description(
        p, _("Sound file to play when you finish first."))


def play_sound(media_path: str,
               monitoring_type: int = obs.OBS_MONITORING_TYPE_MONITOR_ONLY):
    with media_source_ar(media_path, monitoring_type) as media_source:
        obs.obs_set_output_source(63, media_source)
