import obspython as obs
from rtgg_obs import RacetimeObs
from . import fill_source_list


def script_coop_settings(props, rtgg_obs: RacetimeObs):
    p = obs.obs_properties_add_bool(
        props, "use_coop", "Display coop information?")
    obs.obs_property_set_modified_callback(p, coop_toggled)
    coop_group = obs.obs_properties_create()
    obs.obs_properties_add_group(
        props, "coop_group", "Co-op Mode", obs.OBS_GROUP_NORMAL, coop_group
    )
    obs.obs_property_set_visible(
        obs.obs_properties_get(props, "coop_group"), rtgg_obs.coop.enabled)
    p = obs.obs_properties_add_list(
        coop_group, "coop_partner", "Co-op Partner",
        obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING
    )
    p = obs.obs_properties_add_list(
        coop_group, "coop_opponent1", "Co-op Opponent 1",
        obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING
    )
    p = obs.obs_properties_add_list(
        coop_group, "coop_opponent2", "Co-op Opponent 2",
        obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING
    )
    fill_coop_entrant_lists(props, rtgg_obs)
    p = obs.obs_properties_add_list(
        coop_group, "coop_source", "Coop Text Source",
        obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING
    )
    obs.obs_property_set_long_description(p, (
        "This text source will display the time that the last racer needs to"
        " finish for their team to win"
    ))
    fill_source_list(p)
    p = obs.obs_properties_add_list(
        coop_group, "coop_label", "Coop Label Text Source",
        obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING
    )
    obs.obs_property_set_long_description(p, (
        "This text source will be use to display a label such as "
        "\'<PartnerName> needs to finish before\' based on who the last racer"
        " is"
    ))
    fill_source_list(p)


def coop_toggled(props, prop, settings):
    vis = obs.obs_data_get_bool(settings, "use_coop")
    obs.obs_property_set_visible(
        obs.obs_properties_get(props, "coop_group"), vis)
    return True


def fill_coop_entrant_lists(props, rtgg_obs: RacetimeObs):
    fill_entrant_list(
        rtgg_obs.race, obs.obs_properties_get(props, "coop_partner"))
    fill_entrant_list(rtgg_obs.race, obs.obs_properties_get(
        props, "coop_opponent1"))
    fill_entrant_list(rtgg_obs.race, obs.obs_properties_get(
        props, "coop_opponent2"))


def fill_entrant_list(race, entrant_list):
    obs.obs_property_list_clear(entrant_list)
    obs.obs_property_list_add_string(entrant_list, "", "")
    if race is not None:
        for entrant in race.entrants:
            obs.obs_property_list_add_string(
                entrant_list, entrant.user.full_name, entrant.user.full_name)


def script_update_coop_settings(settings, rtgg_obs: RacetimeObs):
    rtgg_obs.coop.enabled = obs.obs_data_get_bool(settings, "use_coop")
    rtgg_obs.coop.partner = obs.obs_data_get_string(settings, "coop_partner")
    rtgg_obs.coop.opponent1 = obs.obs_data_get_string(
        settings, "coop_opponent1")
    rtgg_obs.coop.opponent2 = obs.obs_data_get_string(
        settings, "coop_opponent2")
    rtgg_obs.coop.source = obs.obs_data_get_string(settings, "coop_source")
    rtgg_obs.coop.label_source = obs.obs_data_get_string(
        settings, "coop_label")
