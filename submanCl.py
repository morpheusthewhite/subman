#!/usr/bin/env python

from sys import argv
from bin.settingUtil import *
from bin import playUtil

###---Command line version of subman---###

# TODO: use argparse
# TODO: give the user the possibility to play last video

if len(argv) > 1 and argv[1] == "-h" :
    print("Script for launching videos with subs in specified folders. Reminds of the last episode watched")
    print("Configure usage: subman PATH_TO_VIDEOS PATH_TO_SUBS")
    print("Next usages: subman")
    print("If called with two arguments sets it as new video and sub folder")
    print("The specified folders must contains only videos and subs (they cannot be in the same)")
    exit()
elif len(argv) > 2:
    print("Specified some path, creating setting file...")
    createSettingAndCountFile(argv[1], argv[2])
elif not existSettingAndCountFile():
    print("Setting file does not exist and too few arguments")
    print("Errore: paths unspecified. -h for help")
    exit()

import subprocess

(count, pathToVideo, pathToSubs, videoPattern, subsPattern) = readSetting()

print("Calculating next video and next subtitles file")
(nextVid, nextSub) = playUtil.getNext(pathToVideo, videoPattern, pathToSubs, subsPattern, count)

if nextVid is None and nextSub is None:
    print("No more files are available, exiting...")
    exit(1)

print("Launching vlc...")
vlc_args = ["vlc", "--fullscreen", "--sub-file", nextSub, "--play-and-exit", nextVid]
vlc = subprocess.Popen(vlc_args)
vlc.wait()

# TODO: manage real end of the video and end of the application

print("Updating count file...")
updateCountFile(count)
