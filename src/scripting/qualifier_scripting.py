import obspython as obs
from rtgg_obs import RacetimeObs
from . import fill_source_list


def script_qualifier_settings(props, rtgg_obs: RacetimeObs):
    p = obs.obs_properties_add_bool(
            props, "use_qualifier",
            "Display race results as tournament qualifier?"
        )
    obs.obs_property_set_modified_callback(p, qualifier_toggled)
    qualifier_group = obs.obs_properties_create()
    obs.obs_properties_add_group(
            props, "qualifier_group", "Qualifier Mode",
            obs.OBS_GROUP_NORMAL, qualifier_group
        )
    obs.obs_property_set_visible(
        obs.obs_properties_get(props, "qualifier_group"),
        rtgg_obs.qualifier.enabled
    )
    p = obs.obs_properties_add_int_slider(
            qualifier_group, "qualifier_cutoff",
            "Use Top X as par time, where X=", 3, 10, 1
        )
    p = obs.obs_properties_add_list(
            qualifier_group,
            "qualifier_par_source",
            "Qualifier Par Time Source",
            obs.OBS_COMBO_TYPE_EDITABLE,
            obs.OBS_COMBO_FORMAT_STRING
        )
    fill_source_list(p)
    p = obs.obs_properties_add_list(
            qualifier_group,
            "qualifier_score_source",
            "Qualifier Score Source",
            obs.OBS_COMBO_TYPE_EDITABLE,
            obs.OBS_COMBO_FORMAT_STRING
        )
    fill_source_list(p)


def qualifier_toggled(props, prop, settings):
    vis = obs.obs_data_get_bool(settings, "use_qualifier")
    obs.obs_property_set_visible(
        obs.obs_properties_get(props, "qualifier_group"), vis)
    return True


def script_update_qualifier_settings(settings, rtgg_obs: RacetimeObs):
    rtgg_obs.qualifier.enabled = obs.obs_data_get_bool(
        settings, "use_qualifier")
    rtgg_obs.qualifier.qualifier_cutoff = obs.obs_data_get_int(
        settings, "qualifier_cutoff")
    rtgg_obs.logger.debug(
        f"qualifier_cutoff is {rtgg_obs.qualifier.qualifier_cutoff}")
    rtgg_obs.qualifier.par_source = obs.obs_data_get_string(
        settings, "qualifier_par_source")
    rtgg_obs.qualifier.score_source = obs.obs_data_get_string(
        settings, "qualifier_score_source")
