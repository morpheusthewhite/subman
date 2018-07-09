import os

# returns 2 strings, the first and the second part of the name (without the episode
# number), and an Integer (the number of files available)
def getPattern(path, isVideo):
    videos = os.listdir(path)

    clearedVideos = []

    if isVideo:
        extensions = (".mkv", ".avi", ".mp4", ".mpeg", ".flv", ".wmv")
    else:
        extensions = (".srt", ".vtt", ".scc")

    for file in videos:
        if not os.path.isdir(path+file) and file.endswith(extensions):
            clearedVideos.append(file)

    nAvailable = len(clearedVideos)
    clearedVideos.sort()
    firstVideo = clearedVideos[0]

    if nAvailable == 1:
        return "", firstVideo, 1

    secondVideo = clearedVideos[1]

    for i in range(len(firstVideo)-1, 0, -1):
        match = firstVideo[i-1]+firstVideo[i]
        if match == "01" and secondVideo[i-1]+secondVideo[i] == "02":
            return firstVideo[:i-1], firstVideo[i+1:], nAvailable


SEPARATING_PATTERN = "____"
