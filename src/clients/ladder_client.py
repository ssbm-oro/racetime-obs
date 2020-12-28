from typing import Any

import requests

from models.ladder import (Standings, flags_from_dict, racer_results_from_dict,
                           racers_from_dict, schedule_from_dict,
                           seasons_from_dict, standings_from_dict)


def script_description():
    return (
        "<p>You've loaded the incorrect script.<br><br>Please remove this file"
        "and add 'racetime_obs.py' instead</p>"
    )


base_url = "https://alttprladder.com/api/v1/PublicApi/"


def ladder_get(uri: str, payload={}):
    headers = {
        'User-Agent': "oro-obs-bot_alpha"
    }
    try:
        with requests.get(uri, payload, headers=headers) as res:
            if res.status_code == 200:
                try:
                    return res.json()
                except ValueError:
                    # GetCurrentRaceTime isn't returned in json
                    return res.text
    except Any:
        return None


def get_active_racers():
    return racers_from_dict(ladder_get(f'{base_url}GetActiveRacers'))


def get_flags():
    return flags_from_dict(ladder_get(f'{base_url}GetFlags'))


def get_seasons():
    return seasons_from_dict(ladder_get(f'{base_url}GetSeasons'))


def get_standings(season_id=0, flag_id=0):
    payload = {"season_id": season_id, "flag_id": flag_id}
    return standings_from_dict(ladder_get(f'{base_url}GetStandings', payload))


def get_racer_standings(racer_id, season_id=0, flag_id=0):
    payload = {
        "racer_id": racer_id,
        "season_id": season_id,
        "flag_id": flag_id
    }
    return (Standings.from_dict(
        ladder_get(f'{base_url}GetRacerStandings', payload)
        ))


def get_racer_history(racer_id):
    payload = {"racer_id": racer_id}
    return racer_results_from_dict(
        ladder_get(f'{base_url}GetRacerHistory', payload))


def get_schedule():
    return schedule_from_dict(ladder_get(f'{base_url}GetSchedule'))


def get_current_race_time():
    return ladder_get(f'{base_url}GetCurrentRaceTime')
