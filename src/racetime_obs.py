from threading import Thread
from typing import List

import obspython as obs
import racetime_client
from helpers.obs_context_manager import (
    data_ar, source_ar
)
from models.category import Category
from models.race import Race
from rtgg_obs import RacetimeObs

from scripting import fill_source_list
import scripting.setup_scripting as setup_scripting
import scripting.timer_scripting as timer_scripting
import scripting.coop_scripting as coop_scripting
import scripting.qualifier_scripting as qualifier_scripting
import scripting.media_player_scripting as media_player_scripting

rtgg_obs = RacetimeObs()


def script_description():
    return (
        "<center><p>Select a text source to use as your timer and enter your"
        "full username on racetime.gg  (including discriminator). This only"
        "needs to be done once.\n\nThen select the race room each race you "
        "join and stop worrying about whether you started your timer or not."
        "<hr/></p>"
    )


def script_load(settings):
    rtgg_obs.timer.use_podium_colors = obs.obs_data_get_bool(
        settings, "use_podium")

    race_update_t = Thread(target=rtgg_obs.race_update_thread)
    race_update_t.daemon = True
    race_update_t.start()


def script_save(settings):
    obs.obs_data_set_bool(settings, "use_podium",
                          rtgg_obs.timer.use_podium_colors)


def script_update(settings):
    setup_scripting.script_update_setup_settings(settings, rtgg_obs)
    timer_scripting.script_update_timer_settings(
        settings, rtgg_obs, update_sources
    )
    coop_scripting.script_update_coop_settings(settings, rtgg_obs)
    qualifier_scripting.script_update_qualifier_settings(settings, rtgg_obs)
    media_player_scripting.script_update_media_player_settings(
        settings, rtgg_obs
    )

    rtgg_obs.full_name = obs.obs_data_get_string(settings, "username")

    rtgg_obs.timer.source_name = obs.obs_data_get_string(settings, "source")

    rtgg_obs.selected_race = obs.obs_data_get_string(settings, "race")
    rtgg_obs.category = obs.obs_data_get_string(settings, "category_filter")


def script_defaults(settings):
    obs.obs_data_set_default_string(settings, "race_info", "Race info")
    obs.obs_data_set_default_string(settings, "race", "")
    obs.obs_data_set_default_int(settings, "qualifier_cutoff", 3)


def script_properties():
    props = obs.obs_properties_create()
    setup_scripting.script_setup(
        props, new_race_selected, new_category_selected
    )

    refresh = obs.obs_properties_add_button(
        props, "button", "Refresh", lambda *props: None)
    obs.obs_property_set_modified_callback(refresh, refresh_pressed)
    timer_scripting.script_timer_settings(props, rtgg_obs,)
    coop_scripting.script_coop_settings(props, rtgg_obs)
    qualifier_scripting.script_qualifier_settings(props, rtgg_obs)
    media_player_scripting.script_media_player_settings(
        props, rtgg_obs, media_player_toggled
    )

    return props


def refresh_pressed(props, prop, *args, **kwargs):
    fill_source_list(obs.obs_properties_get(props, "source"))
    fill_source_list(obs.obs_properties_get(props, "coop_label"))
    fill_source_list(obs.obs_properties_get(props, "coop_text"))
    fill_source_list(obs.obs_properties_get(props, "qualifier_par_source"))
    fill_source_list(obs.obs_properties_get(props, "qualifier_score_source"))
    fill_race_list(obs.obs_properties_get(props, "race"),
                   obs.obs_properties_get(props, "category_filter"))
    if rtgg_obs.race is not None:
        rtgg_obs.coop.update_coop_text(rtgg_obs.race, rtgg_obs.full_name)
        update_coop_sources()
        rtgg_obs.qualifier.update_qualifier_text(
            rtgg_obs.race, rtgg_obs.full_name)
        rtgg_obs.media_player.race_updated(rtgg_obs.race)
    return True


def new_race_selected(props, prop, settings):
    rtgg_obs.selected_race = obs.obs_data_get_string(settings, "race")
    r = racetime_client.get_race_by_name(rtgg_obs.selected_race)
    if r is not None:
        rtgg_obs.race = r
        rtgg_obs.coop.update_coop_text(rtgg_obs.race, rtgg_obs.full_name)
        rtgg_obs.qualifier.update_qualifier_text(
            rtgg_obs.race, rtgg_obs.full_name)
        rtgg_obs.media_player.race_updated(rtgg_obs.race)
        rtgg_obs.logger.info(f"new race selected: {rtgg_obs.race}")
        obs.obs_data_set_default_string(settings, "race_info", r.info)
        coop_scripting.fill_coop_entrant_lists(props, rtgg_obs)
    else:
        obs.obs_data_set_default_string(
            settings, "race_info", "Race not found")

    rtgg_obs.race_changed = True
    return True


def new_category_selected(props, prop, settings):
    rtgg_obs.category = obs.obs_data_get_string(settings, "category_filter")
    rtgg_obs.logger.info(f"new category selected: {rtgg_obs.category}")
    fill_race_list(obs.obs_properties_get(props, "race"), prop)
    return True


def media_player_toggled(props, prop, settings):
    vis = obs.obs_data_get_bool(settings, "use_media_player")
    obs.obs_property_set_visible(
        obs.obs_properties_get(props, "media_player_group"), vis)
    return True


def update_sources():
    if rtgg_obs.race is not None:
        if rtgg_obs.timer.is_enabled():
            color, time = rtgg_obs.timer.get_timer_text(
                rtgg_obs.race, rtgg_obs.full_name)
            set_source_text(rtgg_obs.timer.source_name, time, color)
        update_coop_sources()
        if rtgg_obs.qualifier.is_enabled():
            set_source_text(rtgg_obs.qualifier.par_source,
                            rtgg_obs.qualifier.par_text, None)
            set_source_text(rtgg_obs.qualifier.score_source,
                            rtgg_obs.qualifier.entrant_score, None)
        if rtgg_obs.media_player.enabled:
            rtgg_obs.media_player.race_updated(rtgg_obs.race)


def update_coop_sources():
    if rtgg_obs.coop.is_enabled():
        rtgg_obs.coop.update_coop_text(rtgg_obs.race, rtgg_obs.full_name)
        set_source_text(
            rtgg_obs.coop.our_time_source,
            rtgg_obs.coop.our_time_text,
            rtgg_obs.coop.our_time_color
        )
        set_source_text(
            rtgg_obs.coop.opponent_time_source,
            rtgg_obs.coop.opponent_time_text,
            rtgg_obs.coop.opponent_time_color
        )


def update_coop_sources():
    if rtgg_obs.coop.is_enabled():
        rtgg_obs.coop.update_coop_text(rtgg_obs.race, rtgg_obs.full_name)
        set_source_text(
            rtgg_obs.coop.our_time_source,
            rtgg_obs.coop.our_time_text,
            rtgg_obs.coop.our_time_color
        )
        set_source_text(
            rtgg_obs.coop.opponent_time_source,
            rtgg_obs.coop.opponent_time_text,
            rtgg_obs.coop.opponent_time_color
        )


def update_coop_sources():
    if rtgg_obs.coop.is_enabled():
        rtgg_obs.coop.update_coop_text(rtgg_obs.race, rtgg_obs.full_name)
        set_source_text(
            rtgg_obs.coop.our_time_source,
            rtgg_obs.coop.our_time_text,
            rtgg_obs.coop.our_time_color
        )
        set_source_text(
            rtgg_obs.coop.opponent_time_source,
            rtgg_obs.coop.opponent_time_text,
            rtgg_obs.coop.opponent_time_color
        )


def fill_race_list(race_list, category_list):
    obs.obs_property_list_clear(race_list)
    obs.obs_property_list_clear(category_list)
    obs.obs_property_list_add_string(category_list, "All", "All")

    obs.obs_property_list_add_string(race_list, "", "")
    races = racetime_client.get_races()
    if races is not None:
        fill_category_list(category_list, races)
        for race in filter_races_by_category(races, rtgg_obs.category):
            obs.obs_property_list_add_string(race_list, race.name, race.name)


def fill_category_list(category_list, races: List[Race]):
    categories = []
    for race in races:
        if race.category.name not in categories:
            categories.append(race.category.name)
            obs.obs_property_list_add_string(
                category_list, race.category.name, race.category.name)


def filter_races_by_category(races: List[Race], category: Category) -> Race:
    for race in races:
        if (
            rtgg_obs.category == "" or rtgg_obs.category == "All" or
            race.category.name == rtgg_obs.category
        ):
            yield race


def set_source_text(source_name: str, text: str, color: int):
    if source_name is None or source_name == "":
        return
    # copied and modified from scripted-text.py by UpgradeQ
    with source_ar(source_name) as source, data_ar() as settings:
        obs.obs_data_set_string(settings, "text", text)
        source_id = obs.obs_source_get_unversioned_id(source)
        if color is not None:
            if source_id == "text_gdiplus":
                obs.obs_data_set_int(settings, "color", color)  # colored text

            # freetype2 is BGR, should be reversed for getting correct color
            else:
                number = "".join(hex(color)[2:])
                color = int("0xff" f"{number}", base=16)
                obs.obs_data_set_int(settings, "color1", color)

        obs.obs_source_update(source, settings)
