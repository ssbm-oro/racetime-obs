# flake8: noqa
import random
from datetime import datetime, timedelta
from typing import List

from models.race import Entrant, Status
from models.user import User

# sample of real users that were in the largest race i could find in my race history
test_users = [
    User(id='N5zbdeWe64BYPK8O', full_name='matt7898#1275', name='matt7898', url='/user/N5zbdeWe64BYPK8O', discriminator='1275', stats=None, pronouns=None, flair='',
         twitch_name='matt7898', twitch_display_name='matt7898', twitch_channel='https://www.twitch.tv/matt7898', can_moderate=False, avatar='https://racetime.gg/media/darklink-min_2.jpg'),
    User(id='ZbpNAaBv7d3Jkg04', full_name='Linlinlin', name='Linlinlin', url='/user/ZbpNAaBv7d3Jkg04', discriminator=None, stats=None, pronouns='he/him', flair='supporter',
         twitch_name='linlinlinnya', twitch_display_name='LinlinlinNya', twitch_channel='https://www.twitch.tv/linlinlinnya', can_moderate=False, avatar='https://racetime.gg/media/Pecoprofilepic.png'),
    User(id='pRbOXG3yYP3ZVKq1', full_name='Gammachuu#1618', name='Gammachuu', url='/user/pRbOXG3yYP3ZVKq1', discriminator='1618', stats=None, pronouns='he/him', flair='',
         twitch_name='gammachuu', twitch_display_name='Gammachuu', twitch_channel='https://www.twitch.tv/gammachuu', can_moderate=False, avatar='https://racetime.gg/media/Hi_Pikachu.jpg'),
    User(id='XGzr7pBMO6okqgyE', full_name='zerorush#7264', name='zerorush', url='/user/XGzr7pBMO6okqgyE', discriminator='7264', stats=None, pronouns=None,
         flair='', twitch_name='zer0rush', twitch_display_name='zer0rush', twitch_channel='https://www.twitch.tv/zer0rush', can_moderate=False, avatar=None),
    User(id='AEk8wpokadB5KQyV', full_name='Kyong#9403', name='Kyong', url='/user/AEk8wpokadB5KQyV', discriminator='9403', stats=None, pronouns='he/him', flair='',
         twitch_name='kyong92', twitch_display_name='Kyong92', twitch_channel='https://www.twitch.tv/kyong92', can_moderate=False, avatar='https://racetime.gg/media/kyong_uwa.jpg'),
    User(id='NJrM6PoYDk3Rdm5v', full_name='P-Train#3117', name='P-Train', url='/user/NJrM6PoYDk3Rdm5v', discriminator='3117', stats=None, pronouns='he/him', flair='moderator',
         twitch_name='ptrain24', twitch_display_name='ptrain24', twitch_channel='https://www.twitch.tv/ptrain24', can_moderate=True, avatar='https://racetime.gg/media/ptrainOtter_-_sml.png'),
    User(id='XGzr7pBM82WkqgyE', full_name='Rayvis#1601', name='Rayvis', url='/user/XGzr7pBM82WkqgyE', discriminator='1601', stats=None, pronouns='he/him', flair='',
         twitch_name='rayvis10', twitch_display_name='Rayvis10', twitch_channel='https://www.twitch.tv/rayvis10', can_moderate=False, avatar='https://racetime.gg/media/Cloud_Portrait.jpg'),
    User(id='17DexWE8Zpoak64R', full_name='Pennyroyal_Oil#1056', name='Pennyroyal_Oil', url='/user/17DexWE8Zpoak64R', discriminator='1056', stats=None, pronouns=None,
         flair='', twitch_name='pennyroyal_oil', twitch_display_name='pennyroyal_oil', twitch_channel='https://www.twitch.tv/pennyroyal_oil', can_moderate=False, avatar=None),
    User(id='VwLN8B8Yqv3Pa52R', full_name='DIVISIGNS#3047', name='DIVISIGNS', url='/user/VwLN8B8Yqv3Pa52R', discriminator='3047', stats=None, pronouns=None,
         flair='', twitch_name='divisigns', twitch_display_name='DIVISIGNS', twitch_channel='https://www.twitch.tv/divisigns', can_moderate=False, avatar=None),
    User(id='d17DexWEYRWak64R', full_name='Ninban#5207', name='Ninban', url='/user/d17DexWEYRWak64R', discriminator='5207', stats=None, pronouns=None, flair='',
         twitch_name='ninban', twitch_display_name='Ninban', twitch_channel='https://www.twitch.tv/ninban', can_moderate=False, avatar='https://racetime.gg/media/avatarx100.png'),
    User(id='k5JlzyB7vQWV4GED', full_name='Mooglecharm#6970', name='Mooglecharm', url='/user/k5JlzyB7vQWV4GED', discriminator='6970', stats=None, pronouns='he/him',
         flair='', twitch_name='mooglecharm', twitch_display_name='mooglecharm', twitch_channel='https://www.twitch.tv/mooglecharm', can_moderate=False, avatar=None),
    User(id='dMqzQPW4MvB1L2R5', full_name='Doctor_Marty_0#0901', name='Doctor_Marty_0', url='/user/dMqzQPW4MvB1L2R5', discriminator='0901', stats=None, pronouns='he/him', flair='',
         twitch_name='doctor_marty_0', twitch_display_name='Doctor_Marty_0', twitch_channel='https://www.twitch.tv/doctor_marty_0', can_moderate=False, avatar='https://racetime.gg/media/download_1_AlyFiZL.png'),
    User(id='k5JlzyB7qQoV4GED', full_name='KillerApp23#1596', name='KillerApp23', url='/user/k5JlzyB7qQoV4GED', discriminator='1596', stats=None, pronouns='he/him', flair='',
         twitch_name='killerapp23', twitch_display_name='KillerApp23', twitch_channel='https://www.twitch.tv/killerapp23', can_moderate=False, avatar='https://racetime.gg/media/FeelsCubsMan.jpg'),
    User(id='rVwLN8B8nEoPa52R', full_name='breve#1524', name='breve', url='/user/rVwLN8B8nEoPa52R', discriminator='1524', stats=None, pronouns='he/him', flair='',
         twitch_name='breve_', twitch_display_name='breve_', twitch_channel='https://www.twitch.tv/breve_', can_moderate=False, avatar='https://racetime.gg/media/hoot.png'),
    User(id='ZVa0eMonKPWl9pyJ', full_name='WaltherIV#4773', name='WaltherIV', url='/user/ZVa0eMonKPWl9pyJ', discriminator='4773', stats=None, pronouns='he/him', flair='',
         twitch_name='waltheriv', twitch_display_name='WaltherIV', twitch_channel='https://www.twitch.tv/waltheriv', can_moderate=False, avatar='https://racetime.gg/media/PeepoBoomer.png'),
    User(id='41jgrbWPz3e7P5QE', full_name='Buane#5757', name='Buane', url='/user/41jgrbWPz3e7P5QE', discriminator='5757', stats=None, pronouns=None,
         flair='', twitch_name='buane', twitch_display_name='Buane', twitch_channel='https://www.twitch.tv/buane', can_moderate=False, avatar=None),
    User(id='17DexWE8Qqoak64R', full_name='FloppyBacon#5798', name='FloppyBacon', url='/user/17DexWE8Qqoak64R', discriminator='5798', stats=None, pronouns=None, flair='', twitch_name='floppy__bacon',
         twitch_display_name='Floppy__Bacon', twitch_channel='https://www.twitch.tv/floppy__bacon', can_moderate=False, avatar='https://racetime.gg/media/Starting_soon.jpg'),
    User(id='ZVa0eMonmp3l9pyJ', full_name='waterleau#8538', name='waterleau', url='/user/ZVa0eMonmp3l9pyJ', discriminator='8538', stats=None, pronouns='he/him', flair='',
         twitch_name='waterleau', twitch_display_name='waterleau', twitch_channel='https://www.twitch.tv/waterleau', can_moderate=False, avatar='https://racetime.gg/media/pogchamp.jpg'),
    User(id='wdm1LPWjmwoEnVx6', full_name='VortexofDoom#1756', name='VortexofDoom', url='/user/wdm1LPWjmwoEnVx6', discriminator='1756', stats=None, pronouns='he/him',
         flair='', twitch_name='vortexofdoom97', twitch_display_name='VortexofDoom97', twitch_channel='https://www.twitch.tv/vortexofdoom97', can_moderate=False, avatar=None),
    User(id='AEk8wpokxZW5KQyV', full_name='McMonkey#7533', name='McMonkey', url='/user/AEk8wpokxZW5KQyV', discriminator='7533', stats=None, pronouns='he/him', flair='', twitch_name='mcmonkey819',
         twitch_display_name='McMonkey819', twitch_channel='https://www.twitch.tv/mcmonkey819', can_moderate=False, avatar='https://racetime.gg/media/thoughtful_monkey.jpg'),
    User(id='1jgrbWPlv1We7P5Q', full_name='Tripp#5534', name='Tripp', url='/user/1jgrbWPlv1We7P5Q', discriminator='5534', stats=None, pronouns=None,
         flair='', twitch_name='trippsc2', twitch_display_name='TrippSC2', twitch_channel='https://www.twitch.tv/trippsc2', can_moderate=False, avatar=None),
    User(id='5K9rm36XA9Wq1aOX', full_name='willwc#5671', name='willwc', url='/user/5K9rm36XA9Wq1aOX', discriminator='5671', stats=None, pronouns='he/him', flair='',
         twitch_name='willwc', twitch_display_name='willwc', twitch_channel='https://www.twitch.tv/willwc', can_moderate=False, avatar='https://racetime.gg/media/willwc.png'),
    User(id='k5JlzyB7MvoV4GED', full_name='Spyweaver#6230', name='Spyweaver', url='/user/k5JlzyB7MvoV4GED', discriminator='6230', stats=None, pronouns='he/him', flair='',
         twitch_name='spyweaver', twitch_display_name='Spyweaver', twitch_channel='https://www.twitch.tv/spyweaver', can_moderate=False, avatar='https://racetime.gg/media/Spyweaver.png'),
    User(id='VXY0eABdLLBLKPnz', full_name='incoherent#6156', name='incoherent', url='/user/VXY0eABdLLBLKPnz', discriminator='6156', stats=None, pronouns='he/him', flair='',
         twitch_name='incoherent', twitch_display_name='incoherent', twitch_channel='https://www.twitch.tv/incoherent', can_moderate=False, avatar='https://racetime.gg/media/yCowk2w.png'),
    User(id='wdm1LPWjkwBEnVx6', full_name='fredAKAderf#3930', name='fredAKAderf', url='/user/wdm1LPWjkwBEnVx6', discriminator='3930', stats=None, pronouns='he/him', flair='',
         twitch_name='fredakaderf', twitch_display_name='fredAKAderf', twitch_channel='https://www.twitch.tv/fredakaderf', can_moderate=False, avatar='https://racetime.gg/media/doc-cropped.jpg'),
    User(id='JXzVwZWqKq35k8eb', full_name='dataplet#7164', name='dataplet', url='/user/JXzVwZWqKq35k8eb', discriminator='7164', stats=None, pronouns='he/him',
         flair='moderator', twitch_name='dataplet01', twitch_display_name='Dataplet01', twitch_channel='https://www.twitch.tv/dataplet01', can_moderate=True, avatar=None),
    User(id='kzM65aWX7do1y8q0', full_name='SEJay#5897', name='SEJay', url='/user/kzM65aWX7do1y8q0', discriminator='5897', stats=None, pronouns='he/him', flair='', twitch_name='sejay_28',
         twitch_display_name='SEJay_28', twitch_channel='https://www.twitch.tv/sejay_28', can_moderate=False, avatar='https://racetime.gg/media/lukeacevedo_beer_videogames-01_1x.png'),
    User(id='jb8GPMWwXbB1nEk0', full_name='Ralen Tankir#4377', name='Ralen Tankir', url='/user/jb8GPMWwXbB1nEk0', discriminator='4377', stats=None, pronouns='he/him', flair='',
         twitch_name='ralen_tankir', twitch_display_name='Ralen_Tankir', twitch_channel='https://www.twitch.tv/ralen_tankir', can_moderate=False, avatar='https://racetime.gg/media/icon_052_01.jpg'),
    User(id='XGzr7pBMzq3kqgyE', full_name='HammerBro#0591', name='HammerBro', url='/user/XGzr7pBMzq3kqgyE', discriminator='0591', stats=None, pronouns='he/him',
         flair='', twitch_name='hammerbro_34', twitch_display_name='HammerBro_34', twitch_channel='https://www.twitch.tv/hammerbro_34', can_moderate=False, avatar=None),
    User(id='kzM65aWXxzW1y8q0', full_name='relkin#5557', name='relkin', url='/user/kzM65aWXxzW1y8q0', discriminator='5557', stats=None, pronouns='he/him', flair='', twitch_name='relkin96',
         twitch_display_name='relkin96', twitch_channel='https://www.twitch.tv/relkin96', can_moderate=False, avatar='https://racetime.gg/media/Small_Player_Icon.png'),
    User(id='bjZ2EGWbdL3YlM65', full_name='ObscureLifeForm#6340', name='ObscureLifeForm', url='/user/bjZ2EGWbdL3YlM65', discriminator='6340', stats=None, pronouns=None,
         flair='', twitch_name='obscurelifeform', twitch_display_name='obscurelifeform', twitch_channel='https://www.twitch.tv/obscurelifeform', can_moderate=False, avatar=None),
    User(id='NJrM6PoYkQBRdm5v', full_name='BrewersFanJP#3858', name='BrewersFanJP', url='/user/NJrM6PoYkQBRdm5v', discriminator='3858', stats=None, pronouns='he/him', flair='',
         twitch_name='brewersfanjp', twitch_display_name='BrewersFanJP', twitch_channel='https://www.twitch.tv/brewersfanjp', can_moderate=False, avatar='https://racetime.gg/media/Dragonite-3.png'),
    User(id='1jgrbWPlgzWe7P5Q', full_name='Leviticus#3121', name='Leviticus', url='/user/1jgrbWPlgzWe7P5Q', discriminator='3121', stats=None, pronouns=None, flair='',
         twitch_name='leviticus00', twitch_display_name='Leviticus00', twitch_channel='https://www.twitch.tv/leviticus00', can_moderate=False, avatar='https://racetime.gg/media/300px-U.svg.png'),
    User(id='0wezlNoAA5omq6db', full_name='SeanRhapsody#5116', name='SeanRhapsody', url='/user/0wezlNoAA5omq6db', discriminator='5116', stats=None, pronouns=None, flair='', twitch_name='seanrhapsody',
         twitch_display_name='SeanRhapsody', twitch_channel='https://www.twitch.tv/seanrhapsody', can_moderate=False, avatar='https://racetime.gg/media/received_338403934048267.webp'),
    User(id='graP6yoadA3lV4zN', full_name='JamesFnX#9072', name='JamesFnX', url='/user/graP6yoadA3lV4zN', discriminator='9072', stats=None, pronouns='he/him',
         flair='', twitch_name='jamesfnx', twitch_display_name='JamesFnX', twitch_channel='https://www.twitch.tv/jamesfnx', can_moderate=False, avatar=None),
    User(id='vrZyM4orOEWqDJX0', full_name='SirLinkalot#8175', name='SirLinkalot', url='/user/vrZyM4orOEWqDJX0', discriminator='8175', stats=None, pronouns='he/him', flair='',
         twitch_name='sirlinkalot', twitch_display_name='SirLinkalot', twitch_channel='https://www.twitch.tv/sirlinkalot', can_moderate=False, avatar='https://racetime.gg/media/a112.png'),
    User(id='JXzVwZWqk435k8eb', full_name='Quizbowl#2624', name='Quizbowl', url='/user/JXzVwZWqk435k8eb', discriminator='2624', stats=None, pronouns=None,
         flair='', twitch_name='quizbowl', twitch_display_name='Quizbowl', twitch_channel='https://www.twitch.tv/quizbowl', can_moderate=False, avatar=None),
    User(id='OR6ym83mKpWPd1Xr', full_name='Kynup#9473', name='Kynup', url='/user/OR6ym83mKpWPd1Xr', discriminator='9473', stats=None, pronouns='he/him',
         flair='', twitch_name='kynup', twitch_display_name='Kynup', twitch_channel='https://www.twitch.tv/kynup', can_moderate=False, avatar=None),
    User(id='VXY0eABde53LKPnz', full_name='BlackWax#5032', name='BlackWax', url='/user/VXY0eABde53LKPnz', discriminator='5032', stats=None, pronouns='he/him', flair='', twitch_name='blackwax143',
         twitch_display_name='blackwax143', twitch_channel='https://www.twitch.tv/blackwax143', can_moderate=False, avatar='https://racetime.gg/media/spin_attack_OSNeA7L.jpg'),
    User(id='yMewn83VNE3405Jv', full_name='OmegAtoisk#0588', name='OmegAtoisk', url='/user/yMewn83VNE3405Jv', discriminator='0588', stats=None, pronouns='he/him',
         flair='', twitch_name='omegatoisk', twitch_display_name='Omegatoisk', twitch_channel='https://www.twitch.tv/omegatoisk', can_moderate=False, avatar=None),
    User(id='VXY0eABdAX3LKPnz', full_name='IrritablePenguin#4578', name='IrritablePenguin', url='/user/VXY0eABdAX3LKPnz', discriminator='4578', stats=None, pronouns='he/him', flair='',
         twitch_name='irritablepenguin', twitch_display_name='IrritablePenguin', twitch_channel='https://www.twitch.tv/irritablepenguin', can_moderate=False, avatar='https://racetime.gg/media/IrritableBrandSmall.jpg'),
    User(id='7nxMQeoxlQoapX0A', full_name='tylersalt#0124', name='tylersalt', url='/user/7nxMQeoxlQoapX0A', discriminator='0124', stats=None, pronouns='he/him', flair='',
         twitch_name='tylersalt', twitch_display_name='Tylersalt', twitch_channel='https://www.twitch.tv/tylersalt', can_moderate=False, avatar='https://racetime.gg/media/tsalt.png'),
    User(id='pRbOXG3yDdBZVKq1', full_name='MrScruffNinjaTuna#6668', name='MrScruffNinjaTuna', url='/user/pRbOXG3yDdBZVKq1', discriminator='6668', stats=None, pronouns='he/him', flair='',
         twitch_name='mrscruffninjatuna', twitch_display_name='MrScruffNinjaTuna', twitch_channel='https://www.twitch.tv/mrscruffninjatuna', can_moderate=False, avatar='https://racetime.gg/media/ArinEeeee.png'),
    User(id='DMLq1oZ0YwBOeQG8', full_name='Logic#5451', name='Logic', url='/user/DMLq1oZ0YwBOeQG8', discriminator='5451', stats=None, pronouns='he/him', flair='', twitch_name='illogical286',
         twitch_display_name='ilLogical286', twitch_channel='https://www.twitch.tv/illogical286', can_moderate=False, avatar='https://racetime.gg/media/pathetic.png'),
    User(id='k5JlzyB7nZWV4GED', full_name='xelnophon#7110', name='xelnophon', url='/user/k5JlzyB7nZWV4GED', discriminator='7110', stats=None, pronouns='they/them',
         flair='', twitch_name='xelnaphon', twitch_display_name='xelnaphon', twitch_channel='https://www.twitch.tv/xelnaphon', can_moderate=False, avatar=None),
    User(id='b52QE8oN53lywqX4', full_name='oro#3531', name='oro', url='/user/b52QE8oN53lywqX4', discriminator='3531', stats=None, pronouns='they/them', flair='', twitch_name='ssbmoro',
         twitch_display_name='SsbmOro', twitch_channel='https://www.twitch.tv/ssbmoro', can_moderate=False, avatar='https://racetime.gg/media/oro_icon_100x100.png'),
    User(id='bjZ2EGWbL53YlM65', full_name='Logikz#6972', name='Logikz', url='/user/bjZ2EGWbL53YlM65', discriminator='6972', stats=None, pronouns='he/him',
         flair='', twitch_name='logikz0', twitch_display_name='logikz0', twitch_channel='https://www.twitch.tv/logikz0', can_moderate=False, avatar=None),
    User(id='7lYZa5B54KW2Vwv9', full_name='Durand#3810', name='Durand', url='/user/7lYZa5B54KW2Vwv9', discriminator='3810', stats=None, pronouns=None, flair='', twitch_name='durand_71421',
         twitch_display_name='Durand_71421', twitch_channel='https://www.twitch.tv/durand_71421', can_moderate=False, avatar='https://racetime.gg/media/Neera_Celeste_-_Avatar2.jpg'),
    User(id='wNZ1KRBOG9B4qAyj', full_name='ganonsgonewild#4489', name='ganonsgonewild', url='/user/wNZ1KRBOG9B4qAyj', discriminator='4489', stats=None, pronouns=None,
         flair='', twitch_name='ganonsgonewild', twitch_display_name='GanonsGoneWild', twitch_channel='https://www.twitch.tv/ganonsgonewild', can_moderate=False, avatar=None),
    User(id='kzM65aWX15B1y8q0', full_name='Revenant#2968', name='Revenant', url='/user/kzM65aWX15B1y8q0', discriminator='2968', stats=None, pronouns=None, flair='',
         twitch_name='rampantrevenant', twitch_display_name='RampantRevenant', twitch_channel='https://www.twitch.tv/rampantrevenant', can_moderate=False, avatar=None),
    User(id='JXzVwZWq7R35k8eb', full_name='timp#4057', name='timp', url='/user/JXzVwZWq7R35k8eb', discriminator='4057', stats=None, pronouns='he/him', flair='',
         twitch_name='timp_', twitch_display_name='timp_', twitch_channel='https://www.twitch.tv/timp_', can_moderate=False, avatar='https://racetime.gg/media/uncleface2_112x112.png'),
    User(id='LNqO2YoL8bo9QEya', full_name='Yoinkerswife#4156', name='Yoinkerswife', url='/user/LNqO2YoL8bo9QEya', discriminator='4156', stats=None, pronouns='she/her', flair='',
         twitch_name='yoinkerswife', twitch_display_name='Yoinkerswife', twitch_channel='https://www.twitch.tv/yoinkerswife', can_moderate=False, avatar='https://racetime.gg/media/karrieavatar2.png'),
    User(id='JrM6PoYZb5WRdm5v', full_name='pool_float_g#7064', name='pool_float_g', url='/user/JrM6PoYZb5WRdm5v', discriminator='7064', stats=None, pronouns='he/him', flair='',
         twitch_name='pool_float_g', twitch_display_name='pool_float_g', twitch_channel='https://www.twitch.tv/pool_float_g', can_moderate=False, avatar='https://racetime.gg/media/Cartoony_Profile_Pic.jpg'),
    User(id='zM65aWXNnd31y8q0', full_name='YEAHBUDDY911#1971', name='YEAHBUDDY911', url='/user/zM65aWXNnd31y8q0', discriminator='1971', stats=None, pronouns=None, flair='', twitch_name='yeahbuddy911', twitch_display_name='yeahbuddy911', twitch_channel='https://www.twitch.tv/yeahbuddy911', can_moderate=False, avatar=None
         )]




def get_test_entrants(random_users, *entrants):
    _entrants = []
    for entrant in entrants:
        _entrants.append(entrant)
    for i in range(len(_entrants), 20):
        _entrants.append(get_test_entrant(next(random_users)))
    return _entrants


def get_test_entrant(
     user: User, status_value="joined", finished_at: datetime = None,
     finish_time: timedelta = None, place: int = None
) -> Entrant:
    return Entrant(
         user=user, status=get_test_status(status_value),
         has_comment=False, stream_live=True, stream_override=False,
         actions=[], finished_at=finished_at, finish_time=finish_time,
         place=place
     )


def get_test_status(status_value):
    return Status(value=status_value, verbose_value="", help_text="")
