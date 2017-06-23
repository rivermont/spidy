'''
GUI for spidy Web Crawler
Built by rivermont and FalconWarriorr
'''

'''
TODO:
 - Window with configuration options for various spidy arguments.
 - Start/Pause/Stop button that runs the crawler with given args
 - Console window
 - Bar with active task (link being crawled, etc.)
'''

import tkinter
import crawler.py as spidy

def run_spidy():
	spidy.main()