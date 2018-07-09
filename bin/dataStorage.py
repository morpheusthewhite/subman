class DataStorage():
    # class used to store play informations in gui
    def __init__(self, count, videoPath, videoPattern, subsPath, subsPattern, nAvailable):
        super().__init__()
        self.count = count
        self.videoPath = videoPath
        self.videoPattern = videoPattern
        self.subsPath = subsPath
        self.subsPattern = subsPattern
        self.nAvailable = nAvailable

    def reconfigure(self, count, videoPath, videoPattern, subsPath, subsPattern, nAvailable):
        self.count = count
        self.videoPath = videoPath
        self.videoPattern = videoPattern
        self.subsPath = subsPath
        self.subsPattern = subsPattern
        self.nAvailable = nAvailable
