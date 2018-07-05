def getNext(vidPath, videoPattern, subPath, subPattern, count):
    import os
    from bin import settingUtil

    # no more files available
    if len(os.listdir(vidPath)) < count or len(os.listdir(subPath)) < count:
        return (None, None)

    if count < 9:
        countMod = "0"+str(count)
    else:
        countMod = str(count)

    videoPs = videoPattern.split(settingUtil.SEPARATING_PATTERN)
    video1 = videoPs[0]
    video2 = videoPs[1]
    if not vidPath[len(vidPath)-1]=='/':
        vidPath+='/'
    nextVideo = vidPath+video1+countMod+video2

    subsPs = subPattern.split(settingUtil.SEPARATING_PATTERN)
    subs1 = subsPs[0]
    subs2 = subsPs[1]
    if not subPath[len(subPath)-1]=='/':
        subPath += '/'
    nextSub = subPath+subs1+countMod+subs2

    return (nextVideo, nextSub)

