from datetime import timedelta
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
    # first_place_sound = obs.obs_data_get_string(settings,
    #  "first_place_sound")
    # if first_place_sound is not None and first_place_sound != "":
    #     rtgg_obs.media_player.remove_trigger(0)
    #     rtgg_obs.media_player.add_trigger(first_place_sound, place_trigger=1)
    #     rtgg_obs.media_player.play_media_callback = play_sound
    debug_sound = obs.obs_data_get_string(settings, "debug_sound")
    if debug_sound is not None and debug_sound != "":
        play_time = timedelta(seconds=-5)
        print(f"setting timer to play {debug_sound} at {play_time})")
        # rtgg_obs.media_player.add_timer(debug_sound, play_time)


def script_media_player_settings(
    props, rtgg_obs: RacetimeObs, media_player_toggled
):
    p = obs.obs_properties_add_bool(
        props, "use_media_player", "Play sound if you win?"
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
        "Play a sound for chat messages?"
    )
    obs.obs_properties_add_path(
        media_player_group, "chat_ping_sound",
        "Sound to play when a new chat message arrives", obs.OBS_PATH_FILE,
        "Audio Files (*.mp3 *.aac *.wav *.wma)", None
    )
    obs.obs_properties_add_path(
        media_player_group, "debug_sound",
        "Sound to play when debugging timer", obs.OBS_PATH_FILE,
        "Audio Files (*.mp3 *.aac *.wav *.wma)", None
    )


def play_sound(media_path: str, use_monitoring: bool = True):
    print(f"trying to play sound {media_path}")
    with media_source_ar(media_path, use_monitoring) as media_source:
        obs.obs_set_output_source(63, media_source)
