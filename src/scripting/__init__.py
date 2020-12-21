from typing import List
from models.race import Race
from models.category import Category
import obspython as obs
from helpers.obs_context_manager import data_ar, source_ar, source_list_ar
from rtgg_obs import RacetimeObs
import racetime_client


def fill_source_list(p):
    obs.obs_property_list_clear(p)
    obs.obs_property_list_add_string(p, "", "")
    with source_list_ar() as sources:
        if sources is not None:
            for source in sources:
                source_id = obs.obs_source_get_unversioned_id(source)
                if (
                    source_id == "text_gdiplus" or
                    source_id == "text_ft2_source"
                ):
                    name = obs.obs_source_get_name(source)
                    obs.obs_property_list_add_string(p, name, name)


def fill_race_list(rtgg_obs: RacetimeObs, race_list, category_list):
    obs.obs_property_list_clear(race_list)
    obs.obs_property_list_clear(category_list)
    obs.obs_property_list_add_string(category_list, "All", "All")

    obs.obs_property_list_add_string(race_list, "", "")
    races = racetime_client.get_races()
    if races is not None:
        fill_category_list(category_list, races)
        for race in filter_races_by_category(
            rtgg_obs, races, rtgg_obs.category
        ):
            obs.obs_property_list_add_string(race_list, race.name, race.name)


def fill_category_list(category_list, races: List[Race]):
    categories = []
    for race in races:
        if race.category.name not in categories:
            categories.append(race.category.name)
            obs.obs_property_list_add_string(
                category_list, race.category.name, race.category.name)


def filter_races_by_category(
    rtgg_obs: RacetimeObs, races: List[Race], category: Category
) -> Race:
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
