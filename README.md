# racetime-obs (working title)

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/ssbm-oro/racetime-obs/test-build) [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/ssbm-oro/racetime-obs/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/ssbm-oro/racetime-obs/?branch=master) [![codecov](https://codecov.io/gh/ssbm-oro/racetime-obs/branch/master/graph/badge.svg?token=UOGW4FNM8J)](https://codecov.io/gh/ssbm-oro/racetime-obs)

## Introduction

> :warning: **This is a relatively new project** :warning: I am testing it as much as I can, but I can't test every possible configuration. Please try it in a casual pickup race a few times before you consider using it in a race that you couldn't afford to lose your stream and local recording (e.g. league or tournament races). Please do let me know if you use it and whether you have issues or not. I think that this should be fairly stable, but I would like confirmation with more data points. :smile: If you do decide to use this in an important race, thank you for your bravery and *any issues you encounter are between you and the tournament admins*.

This is the main code repository for racetime-obs, a plugin to add realtime information from [racetime.gg](https://racetime.gg) to your stream in OBS.

### Features

* Co-op mode: Co-op races will automatically calculate the average finish time of your team when you finish. You can also specify another pair of players as your opponent/rivals. Their average time will automatically calculated and displayed. If one team has finished, the other team's timer will count down how much time they have to still win. If it's too late to still win, it'll count up the average time if the last player finished now.
* Qualifier mode: Calculate the par time and your score when the top 3 have finished using the formula score = 2 - (par time / your time)

#### Experimental Features

* Media player: Automatically play a sound (either on stream, to your speakers, or both) based on race events, such as when the race updates, a chat message is posted, when the race starts counting down, or when you finish. The first version of this release will probably just have options for playing a sound when you finish and when the race starts until a better interface can be developed.

### Ideas for future development

The general goal for this is to enable you to do fun things on your stream with the information from racetime.gg. Informational features that are boring will probably be prioritized behind features that are fun :grin:

* Playing media: Play a sound or video file automatically, like an announcer saying "Ready... GO!" when the race starts or a victory fanfare when you come in first place.
* Friends: Announce or list specified friends' finish times if they're in the same race as you.
* Automatically select a layout or scene depending on what game or mode you are racing.
* Restreamers: Make setup for restreaming easier by pulling the racers' information from the race room.
* Race history: List information from your race history, like current win streak or head-to-head record against current opponent.
* Your idea here!

### Screenshot

![Screenshot of Settings](/img/Screenshot1.png)

![Video demo of Coop Mode](/img/coop_demo.gif)

In this demo, you can see two of the features. The timer has turned gold, indicating that I finished first. Then, once both of our opponents have finished, it shows what time my partner Amarith would have needed to finish at for us to win

![Example of Tournament Qualifier Mode](/img/Screenshot2.png)

Example output when using tournament qualifier mode.

## Setup

1) Install the correct version of Python for your system. On Windows, this is Python 3.6. Note on Windows whether you are using the [64-bit](https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe) or [32-bit version](https://www.python.org/ftp/python/3.6.8/python-3.6.8.exe) of OBS, as you'll need to use the same version of Python which you can find at those links. On macOS, this is [Python 3.7](https://www.python.org/ftp/python/3.7.9/python-3.7.9-macosx10.9.pkg). Note on macOS, you also need to use OBS version 25.0.8. Version 26 broke python scripts for macOS.

2) Download and unzip the [latest release archive](https://github.com/ssbm-oro/racetime-obs/releases/latest/) to any folder

3) Install the correct python requirements with `python -m pip install -r requirements.txt`

4) Start OBS and create a Text Source to use as a timer. You can customize the font and style as much as you please. Note that if you enable Podium Colors, whatever color you choose for your text source will get overwritten.

5) From the OBS menu, select `Tools` -> `Scripts`. Click the Python Settings tab, and click the Browse button. Navigate to and select the folder where you installed Python.

6) Switch back to the Scripts tab and press the `+` button, and add `racetime_obs.py`

7) Enable the `Initial Setup` checkbox and select the text source you created in step 4 from the script properties drop down and type in your racetime.gg username (in the form `username#0000`)

8) (optional) Check the "Use custom color for podium finishes" box to have your timer change color depending on what phase the race is in and what place you finished in.

9) Join a racetime.gg race, and select your race room from the drop down. You can select a category to only show races in that category as well.

## Contact

You can find me on Discord, oro#7777.

Also, follow me on [Twitch](https://www.twitch.com/ssbmoro)!

 ![Twitch Status](https://img.shields.io/twitch/status/ssbmoro)

## Acknowledgments

This project is unaffiliated with racetime.gg and OBS Studio, but wouldn't be possible without the wonderful racetime.gg API and usable OBS scripting support.

Thank you to [bfxdev](https://github.com/bfxdev) and [upgradeQ](https://github.com/upgradeQ), whose OBS scripting tutorials and code I referenced heavily when learning how to integrate with OBS.

* [racetime.gg](https://github.com/racetimeGG/racetime-app)
* [OBS Studio](https://github.com/obsproject/obs-studio)
* [bfxdev's OBS scripts](https://github.com/bfxdev/OBS)
* [OBS Python Scripting Cheatsheet by upgradeQ](https://github.com/upgradeQ/OBS-Studio-Python-Scripting-Cheatsheet-obspython-Examples-of-API)
* [Tips and Tricks For Lua Scripts](https://obsproject.com/forum/threads/tips-and-tricks-for-lua-scripts.132256/#post-491262)
