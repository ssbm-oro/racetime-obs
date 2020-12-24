import obspython as obs
from rtgg_obs import RacetimeObs


def script_update_timer_settings(
    settings, rtgg_obs: RacetimeObs, update_sources
):
    rtgg_obs.timer.use_podium_colors = obs.obs_data_get_bool(
        settings, "use_podium")
    rtgg_obs.timer.pre_color = obs.obs_data_get_int(settings, "pre_color")
    rtgg_obs.timer.first_color = obs.obs_data_get_int(settings, "first_color")
    rtgg_obs.timer.second_color = obs.obs_data_get_int(
        settings, "second_color")
    rtgg_obs.timer.third_color = obs.obs_data_get_int(settings, "third_color")
    rtgg_obs.timer.racing_color = obs.obs_data_get_int(
        settings, "racing_color")
    rtgg_obs.timer.finished_color = obs.obs_data_get_int(
        settings, "finished_color")
    rtgg_obs.logger.debug(f"timer.enabled is {rtgg_obs.timer.enabled}")
    rtgg_obs.logger.debug(f"timer.source_name is {rtgg_obs.timer.source_name}")
    rtgg_obs.logger.debug(f"selected_race is {rtgg_obs.selected_race}")


def script_timer_settings(props, rtgg_obs: RacetimeObs):
    p = obs.obs_properties_add_bool(
        props, "use_podium", "Use custom color for podium finishes?")
    obs.obs_property_set_modified_callback(p, podium_toggled)
    podium_group = obs.obs_properties_create()
    obs.obs_properties_add_group(
        props, "podium_group", "Podium Colors",
        obs.OBS_GROUP_NORMAL, podium_group
    )
    obs.obs_property_set_visible(obs.obs_properties_get(
        props, "podium_group"), rtgg_obs.timer.use_podium_colors)
    obs.obs_properties_add_color(podium_group, "pre_color", "Pre-race:")
    obs.obs_properties_add_color(podium_group, "racing_color", "Still racing:")
    obs.obs_properties_add_color(podium_group, "first_color", "1st place:")
    obs.obs_properties_add_color(podium_group, "second_color", "2nd place:")
    obs.obs_properties_add_color(podium_group, "third_color", "3rd place:")
    obs.obs_properties_add_color(
        podium_group, "finished_color", "After podium:")


def podium_toggled(props, prop, settings):
    vis = obs.obs_data_get_bool(settings, "use_podium")
    obs.obs_property_set_visible(
        obs.obs_properties_get(props, "podium_group"), vis)
    return True
