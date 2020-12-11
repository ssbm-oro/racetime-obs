# racetime-obs

> :warning: **This script is in prerelease.** I do not make any guarantees that it will not crash OBS while you are racing. Please do not use it in a race that you couldn't afford to lose your stream and local recording (e.g. league or tournament races).

This is the main code repository for racetime-obs, a plugin to add realtime information from [racetime.gg](https://racetime.gg) to your stream in OBS.

There's not much here yet, check back later.

## Setup

1) Install the correct version of Python for your system. On Windows, this is Python 3.6. Note on Windows whether you are using the 64-bit or 32-bit version of OBS, as you'll need to use the same version of Python. On macOS, this is Python 3.7. Note on macOS, you also need to use OBS version 25.0.8. Version 26 broke python scripts for macOS.

2) Download and unzip source archive to any folder

3) Install the correct python requirements with `python -m pip install -r requirements.txt`

4) Start OBS and create a Text Source to use as a timer. You can customize the font and style as much as you please. Note that if you enable Podium Colors, whatever color you choose for your text source will get overwritten.

5) From the OBS menu, select `Tools` -> `Scripts`. Click the Python Settings tab, and click the Browse button. Navigate to and select the folder where you installed Python.

6) Switch back to the Scripts tab and press the `+` button, and add `timer.py`

7) Select the text source you created in step 4 from the script properties drop down and type in your racetime.gg username (in the form `username#0000`)

8) Join a racetime.gg race, and select your race room from the drop down
