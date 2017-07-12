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

import tkinter
from threading import Thread
from crawler import main

crawlerThread = Thread(target = main)

def runCrawler():
    crawlerThread.start()
