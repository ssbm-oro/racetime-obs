from typing import Any
import requests
import gettext

from models.category import category_from_dict
from models.category_past_races import category_past_races_from_dict
from models.leaderboards import leaderboards_from_dict
from models.race import race_from_dict, races_from_dict
from models.user import user_from_dict
from models.user_past_races import user_past_races_from_dict
from models.user_search import user_search_from_dict


def script_path():
    pass


def script_description():
    localedir = script_path() + "locales"
    lang = gettext.translation("racetime-obs", localedir=localedir)
    _ = lang.gettext
    return (_(
        "<p>You've loaded the incorrect script.<br><br>Please remove this file"
        "and add 'racetime_obs.py' instead</p>"
    ))


base_url = "https://racetime.gg/"


def racetime_get(uri: str, payload={}):
    headers = {
        'User-Agent': "oro-obs-bot_alpha"
    }
    try:
        with requests.get(uri, payload, headers=headers) as res:
            if res.status_code == 200:
                return res.json()
    except Any:
        return None


# Get Races
#
# URL: https://racetime.gg/races/data
# Returns a list of all open and ongoing races.
def get_races():
    return races_from_dict(racetime_get(f'{base_url}races/data'))

# Get Category
#
# URL: https://racetime.gg/<category>/data
# Replace with the category slug, e.g. ootr.
# This endpoint includes all the basic information about the category shown on
# the webpage, except for past races. Current races are given in a summarised
# format, full race information must be retrieved individually.


def get_category(category: str):
    return category_from_dict(racetime_get(f'{base_url}{category}/data'))

# Get Category Past Races
#
# URL: https://racetime.gg/<category>/races/data
# Returns a list of all completed (finished and cancelled) races in a category.
# This list is paginated, and sorted by each race's completion time
# (the ended_at field), most recent first. 10 races are returned per page.


def get_category_past_races(category: str):
    return category_past_races_from_dict(
        racetime_get(f'{base_url}{category}/races/data')
    )

# Get Leaderboard
#
# URL: https://racetime.gg/<category>/leaderboards/data
# Provides category leaderboard data.


def get_leaderboard(category: str):
    return leaderboards_from_dict(racetime_get(
        f'{base_url}{category}/leaderboards/data')
    )

# Get Race Detail
#
# URL: https://racetime.gg/<category>/<race>/data
# Replace with the category slug, e.g. For OoTR use ootr, and with the race
# room identifier, e.g. social-kirby-4429. Typically you'll determine the race
# URL by first retrieving data from one of the other endpoints, which will
# point you directly to this URL. This endpoint covers everything you might
# want to know about a race. All the data shown on  the race page, except for
# chat messages, is provided. A full breakdown of entrants is also  here, which
#  is sorted by race status and finish position, as appropriate.


def get_race(category: str, race: str):
    return race_from_dict(racetime_get(f'{base_url}{category}/{race}/data'))


def get_race_by_name(name: str):
    if name is None or name == "":
        return None
    name = name.replace(base_url, "", 1)
    return race_from_dict(racetime_get(f'{base_url}{name}/data'))

# Get Past User Races
#
# URL: https://racetime.gg/user/<user>/races/data
# Returns a list of all finished (but not cancelled) races that a user has
#  entered. This list is paginated, and sorted by each race's completion time
#  (the ended_at field), most recent first. 10 races are returned per page.


def get_user_past_races(user: str, show_entrants: bool, page: int):
    payload = {"show_entrants": show_entrants, "page": page}
    return user_past_races_from_dict(racetime_get(
        f'{base_url}user/{user}/races/data', payload)
    )

# User Search
#
# URL: https://racetime.gg/user/search
# Returns an array of matching user data blobs.


def search_users(name: str, scrim: str = None):
    payload = {"name": name, "scrim": scrim}
    return user_search_from_dict(racetime_get(
        f'{base_url}/user/search', payload)
    )

# Get User
#
# URL: https://racetime.gg/user/<user>/data


def get_user(name: str):
    endpoint = f'{base_url}/user/{name}/data'
    return user_from_dict(racetime_get(endpoint))
