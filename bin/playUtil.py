import os

import bin.patternRecognition
from bin import settingUtil

def getNext(playInfo, count, nAvailable):
    # no more files available
    if nAvailable < count:
        return (None, None)

    if count <= 9:
        countMod = "0"+str(count)
    else:
        countMod = str(count)

    videoPs = playInfo.videoPattern.split(bin.patternRecognition.SEPARATING_PATTERN)
    video1 = videoPs[0]
    video2 = videoPs[1]
    if not playInfo.videoPath[len(playInfo.videoPath)-1] == '/':
        playInfo.videoPath+='/'
    nextVideo = playInfo.videoPath+video1+countMod+video2

    subsPs = playInfo.subsPattern.split(bin.patternRecognition.SEPARATING_PATTERN)
    subs1 = subsPs[0]
    subs2 = subsPs[1]
    if not playInfo.subsPath[len(playInfo.subsPath)-1] == '/':
        playInfo.subsPath += '/'
    nextSub = playInfo.subsPath+subs1+countMod+subs2

    return (nextVideo, nextSub)


def getNextNoSubs(playInfo, count, nAvailable):
    # no more files available
    if nAvailable < count:
        return (None, None)

    if count < 9:
        countMod = "0"+str(count)
    else:
        countMod = str(count)

    videoPs = playInfo.videoPattern.split(bin.patternRecognition.SEPARATING_PATTERN)
    video1 = videoPs[0]
    video2 = videoPs[1]
    if not playInfo.videoPath[len(playInfo.videoPath)-1] == '/':
        playInfo.videoPath+='/'
    nextVideo = playInfo.videoPath+video1+countMod+video2

    return (nextVideo, "")

