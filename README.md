# racetime-obs (working title)

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/ssbm-oro/racetime-obs/test-build) [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/ssbm-oro/racetime-obs/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/ssbm-oro/racetime-obs/?branch=master) [![codecov](https://codecov.io/gh/ssbm-oro/racetime-obs/branch/master/graph/badge.svg?token=UOGW4FNM8J)](https://codecov.io/gh/ssbm-oro/racetime-obs)

## Introduction

This is the main code repository for racetime-obs, a plugin to add realtime information from [racetime.gg](https://racetime.gg) to your stream in OBS.

### Features

* Co-op mode: Co-op races will automatically calculate the average finish time of your team when you finish. You can also specify another pair of players as your opponent/rivals. Their average time will automatically calculated and displayed. If one team has finished, the other team's timer will count down how much time they have to still win. If it's too late to still win, it'll count up the average time if the last player finished now.
* Qualifier mode: Calculate the par time and your score when the top 3 have finished using the formula score = 2 - (par time / your time)

#### Experimental Features

* Media player: Automatically play a sound (either on stream, to your speakers, or both) based on race events, such as when the race updates, a chat message is posted, when the race starts counting down, or when you finish. Right now, this just has options for playing a sound when you finish or when a bot posts in the channel.
* ALTTPR Ladder mode: Support for timer started by ALTTPR

### Ideas for future development

The general goal for this is to enable you to do fun things on your stream with the information from racetime.gg. Informational features that are boring will probably be prioritized behind features that are fun :grin:

* Friends: Announce or list specified friends' finish times if they're in the same race as you.
* Automatically select a layout or scene depending on what game or mode you are racing.
* Restreamers: Make setup for restreaming easier by pulling the racers' information from the race room.
* Race history: List information from your race history, like current win streak or head-to-head record against current opponent.
* Your idea here!

### Screenshot

![Screenshot of Settings](/img/Screenshot1.png)

![Screenshot of Coop Settings](/img/Screenshot_coop.png)

![Screenshot of Qualifier Settings](/img/Screenshot_qualifier.png)

![Screenshot of Media Player Settings](/img/Screenshot_mediaplayer.png)

![Video demo of Coop Mode](/img/coop_demo2.gif)

In this demo, you can see two of the features. The timer has turned bronze, indicating that I finished third, and also that the average time of [Julloninja](https://twitch.tv/julloninja) and myself is lower than [GanonsGoneWild](http://twitch.tv/ganonsgonewild) (who finished second) and [ZekeHighwind's](https://twitch.tv/zekehighwind) average time if they finished immediately. Therefore, our winning time is colored green while GGW and Zeke's time is red and counts up to show what average time they would have now.

![Example of Tournament Qualifier Mode](/img/Screenshot2.png)

Example output when using tournament qualifier mode.

## Setup

1) Install the correct version of Python for your system. On Windows, this is Python 3.6. Note on Windows whether you are using the [64-bit](https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe) or [32-bit version](https://www.python.org/ftp/python/3.6.8/python-3.6.8.exe) of OBS, as you'll need to use the same version of Python which you can find at those links. On macOS, this is [Python 3.7](https://www.python.org/ftp/python/3.7.9/python-3.7.9-macosx10.9.pkg). Note on macOS, you also need to run [this script](https://cdn.discordapp.com/attachments/670224198991347722/875398835151720448/macos-finder-applications-python3.png) in the Python Applications Directory.

2) Download and unzip the [latest release archive](https://github.com/ssbm-oro/racetime-obs/releases/latest/) to any folder

3) Install the correct python requirements with `python -m pip install -r requirements.txt`

4) Start OBS and create a Text Source to use as a timer. You can customize the font and style as much as you please. Note that if you enable Podium Colors, whatever color you choose for your text source will get overwritten.

5) From the OBS menu, select `Tools` -> `Scripts`. Click the Python Settings tab, and click the Browse button. Navigate to and select the folder where you installed Python.

6) Switch back to the Scripts tab and press the `+` button, and add `racetime_obs.py`

7) Enable the `Initial Setup` checkbox and select the text source you created in step 4 from the script properties drop down and type in your racetime.gg username (in the form `username#0000`)

8) (optional) Check the "Use custom color for podium finishes" box to have your timer change color depending on what phase the race is in and what place you finished in.

9) Join a racetime.gg race, and select your race room from the drop down. You can select a category to only show races in that category as well.

10) (optional) Choose settings for coop mode or qualifier mode if relevant by setting up 2 text sources for each.

## Contact

You can find me on Discord, oro#7777.

Also, follow me on [Twitch](https://www.twitch.com/ssbmoro)! Generally, if I'm racing ALTTPR, then I'm probably using or testing out this plugin and new features in some way.

 ![Twitch Status](https://img.shields.io/twitch/status/ssbmoro)

## Acknowledgments

This project is unaffiliated with racetime.gg and OBS Studio, but wouldn't be possible without the wonderful racetime.gg API and usable OBS scripting support.

Thank you to [bfxdev](https://github.com/bfxdev) and [upgradeQ](https://github.com/upgradeQ), whose OBS scripting tutorials and code I referenced heavily when learning how to integrate with OBS.

* [racetime.gg](https://github.com/racetimeGG/racetime-app)
* [OBS Studio](https://github.com/obsproject/obs-studio)
* [bfxdev's OBS scripts](https://github.com/bfxdev/OBS)
* [OBS Python Scripting Cheatsheet by upgradeQ](https://github.com/upgradeQ/OBS-Studio-Python-Scripting-Cheatsheet-obspython-Examples-of-API)
* [Tips and Tricks For Lua Scripts](https://obsproject.com/forum/threads/tips-and-tricks-for-lua-scripts.132256/#post-491262)
