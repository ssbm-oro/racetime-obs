from helpers.obs_context_manager import media_source_ar
import obspython as obs
from rtgg_obs import RacetimeObs


def script_update_media_player_settings(settings, rtgg_obs: RacetimeObs):
    rtgg_obs.media_player.play_media_callback = play_sound
    rtgg_obs.media_player.enabled = obs.obs_data_get_bool(
        settings, "use_media_player")
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
    p = obs.obs_properties_add_bool(
        props, "use_media_player", "Enable sounds?"
    )
    obs.obs_property_set_modified_callback(p, media_player_toggled)
    media_player_group = obs.obs_properties_create()
    obs.obs_properties_add_group(
            props, "media_player_group", "Media Player Mode",
            obs.OBS_GROUP_NORMAL, media_player_group
        )
    obs.obs_property_set_visible(
        obs.obs_properties_get(props, "media_player_group"),
        rtgg_obs.media_player.enabled
    )
    p = obs.obs_properties_add_bool(
        media_player_group, "use_chat_pings",
        ("Enable this and set choose a sound file to play when a bot posts or "
            "when someone @s you in racetime.gg chat")
    )
    obs.obs_property_set_long_description(
        p, "Play a sound when a chat message arrives?")
    p = obs.obs_properties_add_path(
        media_player_group, "chat_ping_sound",
        "Chat media file", obs.OBS_PATH_FILE,
        "Audio Files (*.mp3 *.aac *.wav *.wma)", None
    )
    obs.obs_properties_add_path(
        media_player_group, "first_place_sound",
        "First Place Sound", obs.OBS_PATH_FILE,
        "Audio Files (*.mp3 *.aac *.wav *.wma)", None
    )
    obs.obs_property_set_long_description(
        p, "Sound file to play when you finish first.")


def play_sound(media_path: str, use_monitoring: bool = True):
    with media_source_ar(media_path, use_monitoring) as media_source:
        obs.obs_set_output_source(63, media_source)
