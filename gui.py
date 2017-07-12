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

mainFrame = ttk.Frame(window, padding='2 2 5 5')
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
