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


# returns 2 strings, the first and the second part of the name (without the episode number)
def getPattern(filename):
    for i in range(len(filename)-1, 0, -1):
        match = filename[i-1]+filename[i]
        if match == "01":
           return filename[:i-1], filename[i+1:]


SEPARATING_PATTERN = "____"


def createSettingAndCountFile(pathVideos, pathSubs):
    with open("count.txt", "w") as f:
        f.write("1") # position

    with open("settings.ini", "w") as f:
        f.write(pathVideos+'\n') # videos folder
        f.write(pathSubs+'\n') # subs folder

        # calculating pattern for videos
        import os
        videos = os.listdir(pathVideos)
        videos.sort()
        firstVideo = videos[0]
        (firstPartVideo, secondPartVideo) = getPattern(firstVideo)
        f.write(firstPartVideo + SEPARATING_PATTERN + secondPartVideo + '\n')

        # calculating pattern for subtitles
        subs = os.listdir(pathSubs)
        subs.sort()
        firstSub = subs[0]
        (firstPartSub, secondPartSub) = getPattern(firstSub)
        f.write(firstPartSub + SEPARATING_PATTERN + secondPartSub + '\n')
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
        pathToSubs = f.readline().strip() # subs folder
        videoPattern = f.readline().strip() # video pattern
        subsPattern = f.readline().strip() # subs pattern

    return count, pathToVid, pathToSubs, videoPattern, subsPattern