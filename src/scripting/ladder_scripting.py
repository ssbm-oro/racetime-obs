from enum import Enum, auto
from typing import List
from models.ladder import Season, Flag

import obspython as obs
from rtgg_obs import RacetimeObs


def _(message):
    return message


class LadderProperties(str, Enum):
    ladder_group = auto()
    ladder_name = auto()
    ladder_season = auto()
    ladder_mode = auto()


lp = LadderProperties


def script_ladder_settings(props, rtgg_obs: RacetimeObs):
    ladder_group = obs.obs_properties_create()
    obs.obs_properties_add_group(
        props, lp.ladder_group, _("Ladder Settings"), obs.OBS_GROUP_NORMAL,
        ladder_group)
    obs.obs_properties_add_text(
        ladder_group, lp.ladder_name, _("Ladder Name"), obs.OBS_TEXT_DEFAULT)
    p = obs.obs_properties_add_list(
        ladder_group, lp.ladder_season, _("Season"), obs.OBS_COMBO_TYPE_LIST,
        obs.OBS_COMBO_FORMAT_STRING
    )
    fill_season_list(p, rtgg_obs.ladder_timer.all_seasons)
    p = obs.obs_properties_add_list(
        ladder_group, lp.ladder_mode, _("Mode"), obs.OBS_COMBO_TYPE_LIST,
        obs.OBS_COMBO_FORMAT_STRING
    )
    fill_mode_list(p, rtgg_obs.ladder_timer.flags)


def script_update_ladder_settings(settings, rtgg_obs: RacetimeObs):
    user_name = obs.obs_data_get_string(settings, lp.ladder_name)
    rtgg_obs.ladder_timer.update_settings(user_name)


def fill_season_list(season_list, seasons: List[Season]):
    obs.obs_property_list_clear(season_list)
    obs.obs_property_list_add_string(season_list, _("All"), "0")
    if seasons is not None:
        for season in seasons:
            obs.obs_property_list_add_string(
                season_list, season.SeasonName, str(season.season_id))


def fill_mode_list(mode_list, modes: List[Flag]):
    obs.obs_property_list_clear(mode_list)
    obs.obs_property_list_add_string(mode_list, _("All"), "0")
    if modes is not None:
        for mode in modes:
            obs.obs_property_list_add_string(
                mode_list, mode.Mode, str(mode.flag_id)
            )
