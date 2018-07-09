from bin.patternRecognition import getPattern, SEPARATING_PATTERN


def existSettingAndCountFile():
    import os
    files = os.listdir(".")
    found = 0

    for file in files:
        if file == "settings.ini" or file == "count.txt":
            found += 1

    if found == 2:
        return True

    return False


def createSettingAndCountFile(pathVideos, pathSubs, withSubs, inFullscreen):
    with open("count.txt", "w") as f:
        f.write("1") # position

    with open("settings.ini", "w") as f:
        f.write(pathVideos+'\n') # videos folder
        f.write(pathSubs+'\n') # subs folder

        # calculating pattern for videos

        ret = getPattern(pathVideos, True)

        if ret is None:
            return -1 # TODO : throw an exception

        (firstPartVideo, secondPartVideo, nAvailable) = ret
        f.write(firstPartVideo + SEPARATING_PATTERN + secondPartVideo + '\n')

        # calculating pattern for subtitles
        if not pathSubs=="":
            ret = getPattern(pathSubs, False)

            if ret is None:
                return -1 # TODO : throw an exception

            (firstPartSub, secondPartSub, subAvailable) = ret

            if subAvailable != nAvailable:
                return -1 # TODO : throw an exception

            f.write(firstPartSub + SEPARATING_PATTERN + secondPartSub + '\n')
        else:
            f.writelines("\n")

        f.writelines([str(withSubs)+'\n', str(inFullscreen)+'\n', str(nAvailable)+'\n'])
    return


def updateCountFile(count):
    with open("count.txt", "w") as f:
        f.write(str(count+1)) # position
    return


def readSetting():
    with open("count.txt", "r") as f:
        count = f.readline().strip()
        count = int(count)

    with open("settings.ini", "r") as f:
        pathToVid = f.readline().strip()  # videos folder
        pathToSubs = f.readline().strip()  # subs folder
        videoPattern = f.readline().strip()  # video pattern
        subsPattern = f.readline().strip()  # subs pattern
        withSubs = f.readline().strip()
        inFullscreen = f.readline().strip()
        nAvailable = int(f.readline().strip())

    return count, pathToVid, pathToSubs, videoPattern, subsPattern, withSubs, inFullscreen, nAvailable