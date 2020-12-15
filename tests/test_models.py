import pytest
import json
from datetime import timedelta, datetime, timezone
from models.race import Race

def test_race1():
    with open('tests/data/race1.txt') as f:
        race = Race.from_dict(json.load(f))
        assert race.name == "alttpr/lazy-hookshot-7357"

def test_finished_race():
    with open('tests/data/finished_race.txt') as f:
        j = json.load(f)
        race = Race.from_dict(j)
        assert race.version == 73
        assert race.name == "alttpr/dazzling-oldman-0937"
        assert race.status.value == "finished"
        assert race.status.verbose_value == "Finished"
        assert race.url == "/alttpr/dazzling-oldman-0937"
        assert race.data_url == "/alttpr/dazzling-oldman-0937/data"
        assert race.websocket_url == "/ws/race/dazzling-oldman-0937"
        assert race.websocket_bot_url == "/ws/o/bot/dazzling-oldman-0937"
        assert race.websocket_oauth_url == "/ws/o/race/dazzling-oldman-0937"
        assert race.category.name == "A Link to the Past Randomizer"
        assert race.category.short_name == "ALttPR"
        assert race.category.slug == "alttpr"
        assert race.category.url == "/alttpr"
        assert race.category.data_url == "/alttpr/data"
        assert race.category.image == "https://racetime.gg/media/alttpr.png"
        assert race.goal.name == "casual xkeys"
        assert race.goal.custom == True
        assert race.info == "crosskeys - https://alttpr.com/h/QJG8VkrjvB - (Flute/Pendant/Magic Powder/Heart/Cape) - Quickswap Enabled"
        assert race.entrants_count == 10
        assert race.entrants_count_finished == 9
        assert race.entrants_count_inactive == 1
        assert len(race.entrants) == race.entrants_count
        assert race.entrants[0].user.id == "kzM65aWX7do1y8q0"
        assert race.entrants[0].user.full_name == "SEJay#5897"
        assert race.entrants[0].user.name == "SEJay"
        assert race.entrants[0].user.discriminator == "5897"
        assert race.entrants[0].user.url == "/user/kzM65aWX7do1y8q0"
        assert race.entrants[0].user.avatar == "https://racetime.gg/media/lukeacevedo_beer_videogames-01_1x.png"
        assert race.entrants[0].user.pronouns == "he/him"
        assert race.entrants[0].user.flair == ""
        assert race.entrants[0].user.twitch_name == "sejay_28"
        assert race.entrants[0].user.twitch_display_name == "SEJay_28"
        assert race.entrants[0].user.twitch_channel == "https://www.twitch.tv/sejay_28"
        assert race.entrants[0].user.can_moderate == False
        assert race.entrants[0].status.value == "done"
        assert race.entrants[0].status.verbose_value == "Finished"
        assert race.entrants[0].finish_time == timedelta(hours=2, minutes=34, seconds=23.909043)
        assert race.entrants[0].finished_at == datetime(2020, 12, 14, 6, 8, 45, 820000, tzinfo=timezone.utc)
        assert race.entrants[0].place == 1
        assert race.entrants[0].place_ordinal == "1st"
        assert race.entrants[0].score == None
        assert race.entrants[0].score_change == None
        assert race.entrants[0].comment == "191"
        assert race.entrants[0].has_comment == True
        assert race.entrants[0].stream_live == False
        assert race.entrants[0].stream_override == False
        assert race.entrants[0].actions == []