#!/usr/bin/python3

###---GUI version of subman---###

from tkinter import *
from tkinter import filedialog, messagebox
import os, bin.settingUtil, bin.playUtil, bin.dataStorage, bin.pathUtil
import subprocess

CURRENT_PATH = bin.pathUtil.calculatePath(os.path.realpath(__file__))


class gui(Tk):
    def __init__(self):
        super(gui, self).__init__()
        self.wm_title("subman")

        # sets the icon
        self.__imgicon__ = PhotoImage(file=os.path.join(CURRENT_PATH, "media", "iconWhite.png"))
        self.tk.call('wm', 'iconphoto', self._w, self.__imgicon__)

        # upperFrame incapsulates everything except the buttons
        self.upperFrame = Frame(self)

        self.selectionFrame = Frame(self.upperFrame)
        # all children of selectionFrame
        self.__initializeVideoFrame__()
        self.__initializeCheckFrame__()
        self.__initializeSubsFrame__()
        self.selectionFrame.pack(side="left", fill="x", expand=True, padx=5)

        self.upperFrame.pack(fill="x", expand=True)

        self.__initializeButtonsFrame__()

        self.center_window(480, 160)

        if bin.settingUtil.existSettingAndCountFile():
            self.__recoverData__()

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
        self.frameSubs.subsPathText = Entry(self.frameSubs, width=30, disabledbackground="dimgrey")
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

    def __initializeCheckFrame__(self):
        self.checkFrame = Frame(self.selectionFrame)
        self.withSubs = IntVar()
        self.withSubs.set(1)
        self.checkFrame.checkbuttonSubs = Checkbutton(self.checkFrame, text="Subtitled", command=self.checkSubsPressed,
                                                      selectcolor="black", variable=self.withSubs) # change here selectcolor if it does not look good (especially in light themes)
        self.checkFrame.checkbuttonSubs.pack(side=LEFT, padx=30)

        self.checkFrame.countLabel = Label(self.checkFrame, text="Count")
        self.checkFrame.countLabel.pack(side=LEFT)
        self.checkFrame.counter = Spinbox(self.checkFrame, width=6, from_=1, increment=1, to=1)
        self.checkFrame.counter.pack(side=LEFT)

        self.inFullscreen = IntVar()
        self.inFullscreen.set(1)
        self.checkFrame.checkbuttonFullscreen = Checkbutton(self.checkFrame, text="Fullscreen", variable=self.inFullscreen,
                                                            selectcolor="black") # change here selectcolor if it does not look good (especially in light themes)
        self.checkFrame.checkbuttonFullscreen.pack(side=LEFT, padx=30)
        self.checkFrame.pack(pady=5)

    def __recoverData__(self):
        # reading saved datas
        (count, videoPath, subsPath, videoPattern, subsPattern, withSubs, inFullscreen, nAvailable) = bin.settingUtil.readSetting()
        if nAvailable > 0:
            self.playInfo = bin.dataStorage.DataStorage(count, videoPath, videoPattern, subsPath, subsPattern, nAvailable)

            # setting text areas with saved text, checkbox and counter limit
            self.frameVideo.videoPathText.insert(END, self.playInfo.videoPath)
            self.frameSubs.subsPathText.insert(END, self.playInfo.subsPath)
            self.setCounter(self.playInfo.count)
            self.inFullscreen.set(inFullscreen)
            self.withSubs.set(withSubs)
            self.checkFrame.counter.configure(to=nAvailable)


    def play(self):
        if not bin.settingUtil.existSettingAndCountFile():
            messagebox.showwarning("Error", "No video specified")
            return

        episodeNumber = int(self.checkFrame.counter.get())

        if self.withSubs.get() == 1:
            (nextVideo, nextSub) = bin.playUtil.getNext(self.playInfo, episodeNumber, self.playInfo.nAvailable)
        else:
            (nextVideo, nextSub) = bin.playUtil.getNextNoSubs(self.playInfo, episodeNumber, self.playInfo.nAvailable)

        if nextVideo is None and nextSub is None:
            messagebox.showwarning("Error", "Video not available in the specified directory")

        vlc_args = ["vlc", "--play-and-exit", nextVideo]

        if self.withSubs.get() == 1:
            vlc_args.append("--sub-file")
            vlc_args.append(nextSub)

        if self.inFullscreen.get() == 1:
            vlc_args.append("--fullscreen")

        vlc = subprocess.Popen(vlc_args)
        vlc.wait()

        bin.settingUtil.updateCountFile(episodeNumber)
        self.playInfo.count = episodeNumber+1
        self.setCounter(self.playInfo.count)

    def apply(self):
        if bin.settingUtil.existSettingAndCountFile():
            response = messagebox.askokcancel(title="Confirm", message="This will replace previous configuration file. Are you sure?")
            if not response:
                return

        if self.frameVideo.videoPathText.get() == "" or (self.withSubs.get() == 1 and self.frameSubs.subsPathText.get() == ""):
            messagebox.showwarning(title="Error", message="Some path are unspecified")
            return

        bin.settingUtil.createSettingAndCountFile(self.frameVideo.videoPathText.get(),
                                                  self.frameSubs.subsPathText.get(), self.withSubs.get(), self.inFullscreen.get())

        (count, videoPath, subsPath, videoPattern, subsPattern, _, _, nAvailable) = bin.settingUtil.readSetting()

        if not hasattr(self, "playInfo"):
            self.playInfo = bin.dataStorage.DataStorage(count, videoPath, videoPattern, subsPath, subsPattern, nAvailable)
        else:
            self.playInfo.reconfigure(count, videoPath, videoPattern, subsPath, subsPattern, nAvailable)

        self.setCounter(self.playInfo.count)
        self.checkFrame.counter.configure(to=nAvailable)

    def reset(self):
        if bin.settingUtil.existSettingAndCountFile():
            response = messagebox.askokcancel(title="Confirm",
                                              message="This will remove previous configuration file. Are you sure?")
            if response:
                os.remove(os.getcwd()+"/count.txt")
                os.remove(os.getcwd()+"/settings.ini")
            else:
                return

        self.frameSubs.subsPathText.delete(0, 'end')  # clears text
        self.frameVideo.videoPathText.delete(0, 'end')  # clears text

        # reset counter
        self.setCounter(1)
        self.checkFrame.counter.configure(to=1)

    def chooseSubs(self):
        text = filedialog.askdirectory(title="Select subs folder", initialdir="~/Videos")
        if not text == ():
            self.frameSubs.subsPathText.delete(0, 'end')  # clears text
            self.frameSubs.subsPathText.insert(END, text)

    def chooseVid(self):
        text = filedialog.askdirectory(title="Select video folder", initialdir="~/Videos")
        if not text == ():
            self.frameVideo.videoPathText.delete(0, 'end')  # clears text
            self.frameVideo.videoPathText.insert(END, text)

    def center_window(self, width=300, height=200):
        # gets screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calculates position x and y coordinates
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def setCounter(self, n):
        self.checkFrame.counter.delete(0, END)
        self.checkFrame.counter.insert(END, n)

    def checkSubsPressed(self):
        if self.withSubs.get() == 0:
            self.frameSubs.subsPathText.configure(state=DISABLED)
            self.frameSubs.subsOpenFolder.configure(state=DISABLED)
        else:
            self.frameSubs.subsPathText.configure(state=NORMAL)
            self.frameSubs.subsOpenFolder.configure(state=NORMAL)


def main():
    mainWindow = gui()
    mainWindow.mainloop()


if __name__ == "__main__":
    main()

