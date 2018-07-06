class DataStorage():
    def __init__(self, count, videoPath, videoPattern, subsPath, subsPattern):
        super().__init__()
        self.count = count
        self.videoPath = videoPath
        self.videoPattern = videoPattern
        self.subsPath = subsPath
        self.subsPattern = subsPattern

    def reconfigure(self, count, videoPath, videoPattern, subsPath, subsPattern):
        self.count = count
        self.videoPath = videoPath
        self.videoPattern = videoPattern
        self.subsPath = subsPath
        self.subsPattern = subsPattern
