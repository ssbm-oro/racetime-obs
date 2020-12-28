from enum import Enum, auto
import gettext

import obspython as obs
from rtgg_obs import RacetimeObs
from gadgets.ladder_timer import LadderTimer


_ = gettext.gettext


class LadderProperties(str, Enum):
    ladder_group = auto()
    ladder_name = auto()


lp = LadderProperties


def script_ladder_settings(props, rtgg_obs: RacetimeObs):
    ladder_group = obs.obs_properties_create()
    p = obs.obs_properties_add_group(
        props, lp.ladder_group, _("Ladder Settings"), obs.OBS_GROUP_NORMAL,
        ladder_group)
    obs.obs_properties_add_text(
        p, lp.ladder_name, _("Ladder Name"), obs.OBS_TEXT_DEFAULT)


def script_update_ladder_settings(settings, ladder_timer: LadderTimer):
    user_name = obs.obs_data_get_string(settings, lp.ladder_name)
    ladder_timer.update_settings(user_name)
