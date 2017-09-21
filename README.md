# vlc_subs_streamer
A simple python script that interfaces with the VLC telnet interface, to broadcast corresponding subtitles to the currently playing video.  

It can handle skipping through the video, pausing, and the currently playing video changing. This script does not need to be started before VLC/the video.

## Setup
Enable the telnet interface as an extra interface, and set the password for it to admin. Leave the port on the default 4212. This can be either done via command line when launching vlc (`vlc --extraintf telnet --telnet-password admin`) or via the Advanced Preferences section in the VLC GUI (Tools->Preferences->Check the all box->Interface->Main interfaces->Lua->Lua Telnet section).  

## Installation

`sudo pip install -r requirements.txt`  

## Running

`python stream.py`  
