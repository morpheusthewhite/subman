import os

# returns 2 strings, the first and the second part of the name (without the episode
# number), and an Integer (the number of files available)
def getPattern(path, isVideo):
    files = os.listdir(path)

    clearedFiles = []

    if isVideo:
        extensions = (".mkv", ".avi", ".mp4", ".mpeg", ".flv", ".wmv")
    else:
        extensions = (".srt", ".vtt", ".scc")

    for file in files:
        if not os.path.isdir(path+file) and file.endswith(extensions):
            clearedFiles.append(file)

    nAvailable = len(clearedFiles)
    clearedFiles.sort()
    firstFile = clearedFiles[0]

    if nAvailable == 1:
        return "", firstFile, 1

    secondFile = clearedFiles[1]

    for i in range(len(firstFile)-1, 0, -1):
        match = firstFile[i-1]+firstFile[i]
        if match == "01" and secondFile[i-1]+secondFile[i] == "02":
            return firstFile[:i-1], firstFile[i+1:], nAvailable


SEPARATING_PATTERN = "____"
