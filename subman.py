#!/usr/bin/python3.6

###---GUI version of subman---###

from tkinter import *
from tkinter import filedialog, messagebox
import os, bin.settingUtil, bin.playUtil, bin.dataStorage, bin.pathUtil
import subprocess, inspect

CURRENT_PATH = bin.pathUtil.calculatePath(os.path.realpath(__file__))


class gui(Tk):
    def __init__(self):
        super(gui, self).__init__()
        self.wm_title("subman")

        #set the icon
        self.__imgicon__ = PhotoImage(file=os.path.join(CURRENT_PATH, "media", "iconWhite.png"))
        self.tk.call('wm', 'iconphoto', self._w, self.__imgicon__)

        self.upperFrame = Frame(self)

        self.selectionFrame = Frame(self.upperFrame)
        self.__initializeVideoFrame__()
        """ WIP
        self.checkbutton = Checkbutton(self, text="Subtitled")
        self.checkbutton.pack(pady=5)
        """
        self.__initializeSubsFrame__()
        self.selectionFrame.pack(side="left", fill="x", expand=True)

        self.__initializeCountFrame()

        self.upperFrame.pack(fill="x", expand=True)

        self.__initializeButtonsFrame__()

        self.center_window(480, 160)

        if bin.settingUtil.existSettingAndCountFile():
            # reading saved datas
            (count, videoPath, subsPath, videoPattern, subsPattern) = bin.settingUtil.readSetting()
            self.playInfo = bin.dataStorage.DataStorage(count, videoPath, videoPattern, subsPath, subsPattern)

            # setting text areas with saved text
            self.frameVideo.videoPathText.insert(END, self.playInfo.videoPath)
            self.frameSubs.subsPathText.insert(END, self.playInfo.subsPath)
            self.setCounter(count)

    def __initializeVideoFrame__(self):
        self.frameVideo = Frame(self.selectionFrame, borderwidth=1, relief="groove")
        self.frameVideo.videoLabel = Label(self.frameVideo, text="Video")
        self.frameVideo.videoLabel.pack(side="left")
        self.frameVideo.videoPathText = Entry(self.frameVideo, width=30)
        self.frameVideo.videoPathText.pack(side="left", padx=4, pady=7, fill="x", expand=True)
        self.frameVideo.videoOpenFolder = Button(self.frameVideo, text="...", height=1, width=1, command=self.chooseVid)
        self.frameVideo.videoOpenFolder.pack(side="right")
        self.frameVideo.pack(pady=5, expand=True, fill="x")

    def __initializeSubsFrame__(self):
        self.frameSubs = Frame(self.selectionFrame, borderwidth=1, relief="groove")
        self.frameSubs.subsLabel = Label(self.frameSubs, text="Subs")
        self.frameSubs.subsLabel.pack(side="left")
        self.frameSubs.subsPathText = Entry(self.frameSubs, width=30)
        self.frameSubs.subsPathText.pack(side="left", padx=4, pady=7, fill="x", expand=True)
        self.frameSubs.subsOpenFolder = Button(self.frameSubs, text="...", height=1, width=1, command=self.chooseSubs)
        self.frameSubs.subsOpenFolder.pack(side="right")
        self.frameSubs.pack(pady=5, expand=True, fill="x")

    def __initializeButtonsFrame__(self):
        self.buttonsFrame = Frame(self)
        self.buttonsFrame.applyButton = Button(self, text="Apply", command=self.apply)
        self.buttonsFrame.applyButton.pack(side="left")
        self.buttonsFrame.playButton = Button(self, text="Play", command=self.play)
        self.__buttonImage__ = PhotoImage(file=os.path.join(CURRENT_PATH, "media", 'playButtonGreen.png'))
        self.buttonsFrame.playButton.config(image=self.__buttonImage__, height=30, width=30)
        self.buttonsFrame.playButton.pack(side="left", padx=120, expand=True)
        self.buttonsFrame.applyButton = Button(self, text="Reset", command=self.reset)
        self.buttonsFrame.applyButton.pack(side="left")
        self.buttonsFrame.pack()

    def __initializeCountFrame(self):
        self.countFrame = Frame(self.upperFrame, borderwidth=1, relief="groove", width=6)
        self.countFrame.countLabel = Label(self.countFrame, text="Count")
        self.countFrame.countLabel.pack()
        self.countFrame.counter = Spinbox(self.countFrame, width=6, from_=1, increment=1, to=10)
        self.countFrame.counter.pack(pady=10)
        self.countFrame.pack(side="right", ipady=10, padx=5)

    def updateStorage(self):
        (count, videoPath, subsPath, videoPattern, subsPattern) = bin.settingUtil.readSetting()
        self.playInfo = bin.dataStorage.DataStorage(count, videoPath, videoPattern, subsPath, subsPattern)

    def play(self):
        if not bin.settingUtil.existSettingAndCountFile():
            messagebox.showwarning("Error", "No video specified")
            return

        episodeNumber = int(self.countFrame.counter.get())

        (nextVideo, nextSub) = bin.playUtil.getNext(self.playInfo.videoPath, self.playInfo.videoPattern, self.playInfo.subsPath,
                             self.playInfo.subsPattern, episodeNumber)

        if nextVideo is None and nextSub is None:
            messagebox.showwarning("Error", "Video not available in the specified directory")

        vlc_args = ["vlc", "--fullscreen", "--sub-file", nextSub, "--play-and-exit", nextVideo]
        vlc = subprocess.Popen(vlc_args)
        vlc.wait()

        bin.settingUtil.updateCountFile(episodeNumber+1)
        self.playInfo.count = episodeNumber+1
        self.setCounter(self.playInfo.count)

    def apply(self):
        if bin.settingUtil.existSettingAndCountFile():
            response = messagebox.askokcancel(title="Confirm", message="This will replace previous configuration file. Are you sure?")
            if response:
                bin.settingUtil.createSettingAndCountFile(self.frameVideo.videoPathText.get(), self.frameSubs.subsPathText.get())
        else:
            bin.settingUtil.createSettingAndCountFile(self.frameVideo.videoPathText.get(),
                                                      self.frameSubs.subsPathText.get())

            (count, videoPath, subsPath, videoPattern, subsPattern) = bin.settingUtil.readSetting()

            if not hasattr(self, "playInfo"):
                self.playInfo = bin.dataStorage.DataStorage(count, videoPath, videoPattern, subsPath, subsPattern)
            else:
                self.playInfo.reconfigure(count, videoPath, videoPattern, subsPath, subsPattern)

    def reset(self):
        if bin.settingUtil.existSettingAndCountFile():
            response = messagebox.askokcancel(title="Confirm",
                                              message="This will remove previous configuration file. Are you sure?")
            if response:
                self.frameSubs.subsPathText.delete(0, 'end')  # clear text
                self.frameVideo.videoPathText.delete(0, 'end')  # clear text
                os.remove(os.getcwd()+"/count.txt")
                os.remove(os.getcwd()+"/settings.ini")

    def chooseSubs(self):
        text = filedialog.askdirectory(title="Select video folder")
        if not text == "":
            self.frameSubs.subsPathText.delete(0, 'end')  # clear text
            self.frameSubs.subsPathText.insert(END, text)


    def chooseVid(self):
        text = filedialog.askdirectory(title="Select subs folder")
        if not text == "":
            self.frameVideo.videoPathText.delete(0, 'end')  # clear text
            self.frameVideo.videoPathText.insert(END, text)

    def center_window(self, width=300, height=200):
        # get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def setCounter(self, n):
        self.countFrame.counter.delete(0, END)
        self.countFrame.counter.insert(END, n)

mainWindow = gui()
mainWindow.mainloop()
