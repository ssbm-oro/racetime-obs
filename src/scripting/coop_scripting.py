import gettext
import os

import obspython as obs
from rtgg_obs import RacetimeObs
from . import fill_source_list


def script_coop_settings(props, rtgg_obs: RacetimeObs):
    lang = gettext.translation(
        "racetime-obs", localedir=os.environ['LOCALEDIR'])
    _ = lang.gettext

    p = obs.obs_properties_add_bool(
        props, "use_coop", _("Display coop information?"))
    obs.obs_property_set_modified_callback(p, coop_toggled)
    coop_group = obs.obs_properties_create()
    obs.obs_properties_add_group(
        props, "coop_group", _("Co-op Mode"), obs.OBS_GROUP_NORMAL, coop_group
    )
    obs.obs_property_set_visible(
        obs.obs_properties_get(props, "coop_group"), rtgg_obs.coop.enabled)
    p = obs.obs_properties_add_list(
        coop_group, "coop_partner", _("Co-op Partner"),
        obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING
    )
    p = obs.obs_properties_add_list(
        coop_group, "coop_opponent1", _("Co-op Rival 1"),
        obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING
    )
    p = obs.obs_properties_add_list(
        coop_group, "coop_opponent2", _("Co-op Rival 2"),
        obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING
    )
    fill_coop_entrant_lists(props, rtgg_obs)
    p = obs.obs_properties_add_list(
        coop_group, "coop_our_source", _("Our Team's Timer"),
        obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING
    )
    obs.obs_property_set_long_description(p, (
        _("This text source will display your team's timer when you finish.")
    ))
    fill_source_list(p)
    p = obs.obs_properties_add_list(
        coop_group, "coop_opponent_source", "Rival Team's Timer",
        obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING
    )
    obs.obs_property_set_long_description(p, (_(
        "This text source will be use to display your rival's timer when "
        "they finish")
    ))
    obs.obs_properties_add_color(
        coop_group, "coop_winner_color", _("Winner Color:"))
    obs.obs_properties_add_color(
        coop_group, "coop_loser_color", _("Loser Color:"))
    obs.obs_properties_add_color(
        coop_group, "coop_undetermined_color", _("Winner Undetermined Color"))
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
    rtgg_obs.coop.our_time_source = (
        obs.obs_data_get_string(settings, "coop_our_source"))
    rtgg_obs.logger.info(f"our_time_sourc is {rtgg_obs.coop.our_time_source}")
    rtgg_obs.coop.opponent_time_source = obs.obs_data_get_string(
        settings, "coop_opponent_source")
    rtgg_obs.coop.winner_color = obs.obs_data_get_int(
        settings, "coop_winner_color")
    rtgg_obs.coop.loser_color = obs.obs_data_get_int(
        settings, "coop_loser_color")
    rtgg_obs.coop.still_racing_color = obs.obs_data_get_int(
        settings, "coop_undetermined_color")
