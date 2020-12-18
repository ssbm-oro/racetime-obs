import random

from models.race import RaceCategory

categories = [
    RaceCategory(
        name='A Link to the Past Randomizer', short_name='ALttPR',
        slug='alttpr', url='/alttpr', data_url='/alttpr/data',
        image='https://racetime.gg/media/alttpr.png'
    ),
    RaceCategory(
        name='Zelda 2 Randomizer', short_name='Z2R', slug='z2r', url='/z2r',
        data_url='/z2r/data',
        image='https://racetime.gg/media/Zelda_II__The_Adventure_of_Link-285x380.jpg'  # noqa: E501
    ),
    RaceCategory(
        name='Ocarina of Time Randomizer', short_name='OoTR', slug='ootr',
        url='/ootr', data_url='/ootr/data',
        image='https://racetime.gg/media/zootr.png'
    )
]


def get_test_race_category():
    return random.choice(categories)
