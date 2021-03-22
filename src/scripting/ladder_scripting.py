import asyncio
from enum import Enum, auto
from gadgets.ladder_timer import LadderTimer

import obspython as obs
from scripting import fill_source_list


def _(message):
    return message


class LadderProperties(str, Enum):
    ladder_group = auto()
    ladder_name = auto()
    ladder_season = auto()
    ladder_mode = auto()
    all_seasons = auto()
    current_season = auto()
    all_modes = auto()
    current_mode = auto()
    stats_source = auto()
    show_season_name = auto()
    show_mode_name = auto()
    show_rating = auto()
    show_rank = auto()
    show_change = auto()
    show_win_loss_tie = auto()
    pre_color = auto()
    racing_color = auto()
    winner_color = auto()
    loser_color = auto()
    ff_color = auto()


lp = LadderProperties
ladder_timer: LadderTimer = None


def script_ladder_settings(props):
    ladder_group = obs.obs_properties_create()
    obs.obs_properties_add_group(
        props, lp.ladder_group, _("Ladder Settings"), obs.OBS_GROUP_NORMAL,
        ladder_group)
    p = obs.obs_properties_add_text(
        ladder_group, lp.ladder_name, _("Ladder Name"), obs.OBS_TEXT_DEFAULT)
    obs.obs_property_set_modified_callback(p, name_modified)
    obs.obs_properties_add_color(
        ladder_group, lp.pre_color, _("Color Pre-Race"))
    obs.obs_properties_add_color(
        ladder_group, lp.racing_color, _("Still Racing Color"))
    obs.obs_properties_add_color(
        ladder_group, lp.winner_color, _("Winner Color"))
    obs.obs_properties_add_color(
        ladder_group, lp.loser_color, _("Loser Color"))
    obs.obs_properties_add_color(
        ladder_group, lp.ff_color, _("Forfeit Color"))
    p = obs.obs_properties_add_list(
            ladder_group, lp.stats_source, _("Ladder Stats Source"),
            obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING
        )
    fill_source_list(p)
    obs.obs_properties_add_bool(
        ladder_group, lp.show_season_name, _("Show Season Name")
    )
    obs.obs_properties_add_bool(
        ladder_group, lp.show_mode_name, _("Show Mode Name")
    )
    obs.obs_properties_add_bool(
        ladder_group, lp.show_rating, _("Show Rating")
    )
    obs.obs_properties_add_bool(
        ladder_group, lp.show_rank, _("Show Rank")
    )
    obs.obs_properties_add_bool(
        ladder_group, lp.show_change, _("Show Change")
    )
    obs.obs_properties_add_bool(
        ladder_group, lp.show_win_loss_tie, _("Show Win/Loss/Tie Record")
    )
    p = obs.obs_properties_add_list(
        ladder_group, lp.ladder_season, _("Season for Stats"),
        obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING
    )
    obs.obs_property_set_modified_callback(p, season_or_mode_changed)
    obs.obs_property_list_add_string(p, _("Lifetime"), "0")
    obs.obs_property_list_add_string(p, _("Current Season"), "-1")
    p = obs.obs_properties_add_list(
        ladder_group, lp.ladder_mode, _("Mode for Stats"),
        obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING
    )
    obs.obs_property_set_modified_callback(p, season_or_mode_changed)
    obs.obs_property_list_add_string(p, _("Global"), "0")
    obs.obs_property_list_add_string(p, _("Current Mode"), "-1")


def script_update_ladder_settings(settings):
    user_name = obs.obs_data_get_string(settings, lp.ladder_name)
    lt = ladder_timer
    lt.update_settings(user_name)
    lt.pre_color = obs.obs_data_get_int(settings, lp.pre_color)
    lt.racing_color = obs.obs_data_get_int(settings, lp.racing_color)
    lt.winner_color = obs.obs_data_get_int(settings, lp.winner_color)
    lt.loser_color = obs.obs_data_get_int(settings, lp.loser_color)
    lt.ff_color = obs.obs_data_get_int(settings, lp.ff_color)
    lt.stats_source = obs.obs_data_get_string(settings, lp.stats_source)
    lt.show_season_name = obs.obs_data_get_bool(settings, lp.show_season_name)
    lt.show_mode_name = obs.obs_data_get_bool(settings, lp.show_mode_name)
    lt.show_rating = obs.obs_data_get_bool(settings, lp.show_rating)
    lt.show_rank = obs.obs_data_get_bool(settings, lp.show_rank)
    lt.show_change = obs.obs_data_get_bool(settings, lp.show_change)
    lt.show_win_loss_tie = obs.obs_data_get_bool(
        settings, lp.show_win_loss_tie)
    lt.season_for_stats = int(
        obs.obs_data_get_string(settings, lp.ladder_season))
    lt.mode_for_stats = int(
        obs.obs_data_get_string(settings, lp.ladder_mode))
    lt.decimals = obs.obs_data_get_bool(settings, "timer_decimals")


def name_modified(props, prop, *args, **kwargs):
    racer_name = obs.obs_data_get_string(args[0], lp.ladder_name)
    p = obs.obs_properties_get(props, lp.ladder_name)
    if ladder_timer.update_settings(racer_name):
        obs.obs_property_set_description(p, _("Ladder Name ✅"))
    else:
        obs.obs_property_set_description(p, _("Ladder Name ❌"))
    return True


def season_or_mode_changed(proprs, prop, *args, **kwargs):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(ladder_timer.update_stats())
    loop.close()
