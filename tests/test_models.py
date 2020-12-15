import pytest
import json
from models.race import Race

def test_race1():
    with open('tests/data/race1.txt') as f:
        race = Race.from_dict(json.load(f))
        assert race.name == "alttpr/lazy-hookshot-7357"