from threading import Thread
import gettext
import os

import obspython as obs
import racetime_client
import scripting.coop_scripting as coop_scripting
import scripting.media_player_scripting as media_player_scripting
import scripting.qualifier_scripting as qualifier_scripting
import scripting.setup_scripting as setup_scripting
import scripting.timer_scripting as timer_scripting
from rtgg_obs import RacetimeObs
from scripting import fill_race_list, fill_source_list, set_source_text

_ = None
rtgg_obs = RacetimeObs()


def script_path():
    # PLACEHOLDER
    # this function gets injected by OBS with actual script path
    pass


def script_description():
    message = _(
        "Select a text source to use as your timer and enter your "
        "full username on racetime.gg  (including discriminator). This "
        "only needs to be done once.\n\nThen select the race room each "
        "race you join and stop worrying about whether you started your "
        "timer or not."
    )
    return (
        "<center>racetime-obs xxVERSIONxx<hr>"
        "<p>" + message + "<hr/></p>"
    )


def script_load(settings):
    rtgg_obs.timer.use_podium_colors = obs.obs_data_get_bool(
        settings, "use_podium")

    rtgg_obs.media_player.last_session_race = obs.obs_data_get_string(
        settings, "last_session_race")

    obs.obs_data_set_string(settings, "race", "None")

    race_update_t = Thread(target=rtgg_obs.race_update_thread)
    race_update_t.daemon = True
    race_update_t.start()


def script_save(settings):
    obs.obs_data_set_bool(settings, "use_podium",
                          rtgg_obs.timer.use_podium_colors)
    obs.obs_data_set_string(
        settings, "last_session_race", rtgg_obs.selected_race)


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
    set_locale()
    obs.obs_data_set_default_string(settings, "race_info", _("Race info"))
    obs.obs_data_set_default_string(settings, "race", "None")
    obs.obs_data_set_default_int(settings, "qualifier_cutoff", 3)


def set_locale():
    global _
    if _ is None:
        os.environ['LOCALEDIR'] = script_path() + "locales"
        os.environ['LANGUAGE'] = obs.obs_get_locale()[0:2]
        lang = gettext.translation(
            "racetime-obs", localedir=os.environ['LOCALEDIR'])
        _ = lang.gettext


def script_properties():
    props = obs.obs_properties_create()
    setup_scripting.script_setup(
        props, new_race_selected, new_category_selected
    )

    refresh = obs.obs_properties_add_button(
        props, "button", _("Refresh"), lambda *props: None)
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
    fill_source_list(obs.obs_properties_get(props, "coop_our_source"))
    fill_source_list(obs.obs_properties_get(props, "coop_opponent_source"))
    fill_source_list(obs.obs_properties_get(props, "qualifier_par_source"))
    fill_source_list(obs.obs_properties_get(props, "qualifier_score_source"))
    fill_race_list(rtgg_obs, obs.obs_properties_get(props, "race"),
                   obs.obs_properties_get(props, "category_filter"))
    if rtgg_obs.race is not None:
        rtgg_obs.coop.update_coop_text(rtgg_obs.race, rtgg_obs.full_name)
        update_coop_sources()
        rtgg_obs.qualifier.update_qualifier_text(
            rtgg_obs.race, rtgg_obs.full_name)
        rtgg_obs.media_player.race_updated(
                rtgg_obs.race, rtgg_obs.full_name)
    return True


def new_race_selected(props, prop, settings):
    set_locale()
    rtgg_obs.race_changed = True
    obs.timer_remove(update_sources)

    rtgg_obs.selected_race = obs.obs_data_get_string(settings, "race")
    if rtgg_obs.selected_race == "None":
        rtgg_obs.race = None
        return True
    r = racetime_client.get_race_by_name(rtgg_obs.selected_race)
    if r is not None:
        rtgg_obs.race = r
        rtgg_obs.coop.update_coop_text(rtgg_obs.race, rtgg_obs.full_name)
        rtgg_obs.qualifier.update_qualifier_text(
            rtgg_obs.race, rtgg_obs.full_name)
        rtgg_obs.media_player.race_updated(
                rtgg_obs.race, rtgg_obs.full_name)
        rtgg_obs.logger.info(f"new race selected: {rtgg_obs.race}")
        obs.obs_data_set_default_string(settings, "race_info", r.info)
        coop_scripting.fill_coop_entrant_lists(props, rtgg_obs)
        rtgg_obs.timer.enabled = True
        obs.timer_add(update_sources, 100)
    else:
        obs.obs_data_set_default_string(
            settings, "race_info", _("Race not found"))
    return True


def new_category_selected(props, prop, settings):
    rtgg_obs.category = obs.obs_data_get_string(settings, "category_filter")
    rtgg_obs.logger.info(f"new category selected: {rtgg_obs.category}")
    fill_race_list(rtgg_obs, obs.obs_properties_get(props, "race"), prop)
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
            rtgg_obs.media_player.race_updated(
                rtgg_obs.race, rtgg_obs.full_name)


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
