# racetime-obs (working title)

## Introduction

> :warning: **This script is in prerelease.** I do not make any guarantees that it will not crash OBS while you are racing. Please do not use yet it in a race that you couldn't afford to lose your stream and local recording (e.g. league or tournament races).

This is the main code repository for racetime-obs, a plugin to add realtime information from [racetime.gg](https://racetime.gg) to your stream in OBS.

What's the point of this? Why not just capture Livesplit or the racetime.gg website? Well, right now there isn't much point and this is really just a proof of concept. The only feature this currently has over those other methods is that you can set your timer's color to change based on what place you come in.But I think there are some other neat and entertaining ideas that this could be used to implement. These are just ideas right now, not plans or features yet. Please let me know if you have any suggestions!

There is also an experimental option for Co-op races which will automatically calculate the finish time of your team and your opponents once 2 or 3 of you have finished and either who won or when the last player needs to finish by to win.

### Ideas for future development

* Playing media: Play a sound or video file automatically, like an announcer saying "Ready... GO!" when the race starts or a victory fanfare when you come in first place.
* Friends: Announce or list specified friends' finish times if they're in the same race as you
* Automatically select a layout or scene depending on what game or mode you are racing.

### Screenshot

![Screenshot of Settings](/img/Screenshot1.png)

![Video demo of Coop Mode](/img/coop_demo.gif)

In this demo, you can see two of the features. The timer has turned gold, indicating that I finished first. Then, once both of our opponents have finished, it shows what time my partner Amarith would have needed to finish at for us to win

## Setup

1) Install the correct version of Python for your system. On Windows, this is Python 3.6. Note on Windows whether you are using the 64-bit or 32-bit version of OBS, as you'll need to use the same version of Python. On macOS, this is Python 3.7. Note on macOS, you also need to use OBS version 25.0.8. Version 26 broke python scripts for macOS.

2) Download and unzip source archive to any folder

3) Install the correct python requirements with `python -m pip install -r requirements.txt`

4) Start OBS and create a Text Source to use as a timer. You can customize the font and style as much as you please. Note that if you enable Podium Colors, whatever color you choose for your text source will get overwritten.

5) From the OBS menu, select `Tools` -> `Scripts`. Click the Python Settings tab, and click the Browse button. Navigate to and select the folder where you installed Python.

6) Switch back to the Scripts tab and press the `+` button, and add `timer.py`

7) Enable the `Initial Setup` checkbox and select the text source you created in step 4 from the script properties drop down and type in your racetime.gg username (in the form `username#0000`)

8) (optional) Check the "Use custom color for podium finishes" box to have your timer change color depending on what phase the race is in and what place you finished in.

9) Join a racetime.gg race, and select your race room from the drop down. You can select a category to only show races in that category as well.

## Acknowledgments

This project is unaffiliated with racetime.gg and OBS Studio, but wouldn't be possible without the wonderful racetime.gg API and usable OBS scripting support.

Thank you to [bfxdev](https://github.com/bfxdev) and [upgradeQ](https://github.com/upgradeQ), whose OBS scripting tutorials and code I referenced heavily when learning how to integrate with OBS.

* [racetime.gg](https://github.com/racetimeGG/racetime-app)
* [OBS Studio](https://github.com/obsproject/obs-studio)
* [bfxdev's OBS scripts](https://github.com/bfxdev/OBS)
* [OBS Python Scripting Cheatsheet by upgradeQ](https://github.com/upgradeQ/OBS-Studio-Python-Scripting-Cheatsheet-obspython-Examples-of-API)
* [Tips and Tricks For Lua Scripts](https://obsproject.com/forum/threads/tips-and-tricks-for-lua-scripts.132256/#post-491262)
