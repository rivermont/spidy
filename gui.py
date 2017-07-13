'''
GUI for spidy Web Crawler
Built by rivermont and FalconWarriorr
'''

'''
 - Window with configuration options for various spidy arguments.
 - Start/Pause/Stop button that runs the crawler with given args
 - Console window
 - Bar with active task (link being crawled, etc.)
'''

from tkinter import *
from tkinter import ttk
from threading import Thread
from crawler import main

crawlerThread = Thread(target = main)

def runCrawler():
    crawlerThread.start()

window = Tk()
window.title('spidy Web Crawler - by rivermont')

mainFrame = ttk.Frame(window, padding='2')
mainFrame.grid(column=0, row=0, sticky=(N, W, E, S))
mainFrame.columnconfigure(0, weight=1)
mainFrame.rowcomfigure(0, weight=1)

Overwrite = BooleanVar()
RaiseErrors = BooleanVar()
SavePages = BooleanVar()
ZipFiles = BooleanVar()
SaveWords = BooleanVar()
TodoFile = StringVar()
DoneFile = StringVar()
LogFile = StringVar()
BadFile = StringVar()
WordFile = StringVar()
SaveCount = IntVar()
MaxNewError = IntVar()

settingBox = ttk.Frame(mainFrame, padding='2', borderwidth=1)
settingBox.grid(column=0, row=0, sticky=(N, S, W))
settingBox.columnconfigure(0, weight=1)
settingBox.rowconfigure(0, weight=1)

rightBar = ttk.Frame(mainFrame, padding='2', borderwidth=1)
rightBar.grid(column=1, row=0, sticky=(N, S, E))
rightBar.columnconfigure(2, weight=1)
rightBar.rowconfigure(0, weight=1)

controlBox = ttk.Frame(rightBar, padding='2')
controlBox.grid(column=?, row=0, sticky=(N, E, W))
controlBox.columnconfigure(?, weight=1)
controlBox.rowconfigure(0, weight=1)

statusBox = ttk.Frame(rightBar, padding='2')
statusBox.grid(column=0, row=1, sticky=(E, W))
statusBox.columnconfigure(0, weight=1)
statusBox.rowconfigure(1, weight=1)

consoleBox = ttk.Frame(rightBar, padding='2')
consoleBox.grid(column=0, row=2)
consoleBox.columnconfigure(0, weight=1)
consoleBox.rowcomfigure(2, weight=1)

pauseButton = ttk.Button(controlBox, padding='2')
pauseButton.grid(column=0, row=0, sticky=(N, S, W))
pauseButton.columnconfigure(0, weight=1)
pauseButton.rowconfigure(0, weight=1)

goButton = ttk.Button(controlBox, padding='2')
goButton.grid(column=1, row=0, sticky=(N, S))
goButton.columnconfigure(1, weight=1)
goButton.rowconfigure(0, weight=1)
