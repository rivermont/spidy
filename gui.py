'''
GUI for spidy Web Crawler
Built by rivermont and FalconWarriorr
'''

############
## IMPORT ##
############

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from threading import Thread
#from crawler import main

#crawlerThread = Thread(target = main)

#def runCrawler():
#    crawlerThread.start()

def get_file():
	return filedialog.askopenfilename()

#Main window
window = Tk()
window.title('spidy Web Crawler - by rivermont')

#Frame to fill main window
mainFrame = ttk.Frame(window, padding='2')
mainFrame.grid(column=0, row=0, sticky=(N, W, E, S))
mainFrame.columnconfigure(0, weight=1)
mainFrame.rowconfigure(0, weight=1)

#Variables
Overwrite = BooleanVar()
RaiseErrors = BooleanVar()
SavePages = BooleanVar()
ZipFiles = BooleanVar()
SaveWords = BooleanVar()
TodoFile = StringVar()
DoneFile = StringVar()
BadFile = StringVar()
WordFile = StringVar()
SaveCount = IntVar()
MaxNewError = IntVar()

#Container to hold variable settings
settingBox = ttk.Frame(mainFrame, padding='2', borderwidth=1)
settingBox.grid(column=0, row=0, sticky=(N, S, W))
settingBox.columnconfigure(0, weight=1)
settingBox.rowconfigure(0, weight=1)

#Container for things on the right side of the main window
rightBar = ttk.Frame(mainFrame, padding='2', borderwidth=1)
rightBar.grid(column=1, row=0, sticky=(N, S, E))
rightBar.columnconfigure(2, weight=1)
rightBar.rowconfigure(0, weight=1)

#Container for controlling the crawler
controlBox = ttk.Frame(rightBar, padding='2', borderwidth=1)
controlBox.grid(column=1, row=0, sticky=(N, E, W))
controlBox.columnconfigure(1, weight=1)
controlBox.rowconfigure(0, weight=1)

#Container for the status elements
statusBox = ttk.Frame(rightBar, padding='2', borderwidth=1)
statusBox.grid(column=0, row=1, sticky=(E, W))
statusBox.columnconfigure(0, weight=1)
statusBox.rowconfigure(1, weight=1)

#Container for the console log
consoleBox = ttk.Frame(rightBar, padding='2', borderwidth=1)
consoleBox.grid(column=0, row=2)
consoleBox.columnconfigure(0, weight=1)
consoleBox.rowconfigure(2, weight=1)

#Button to pause the crawler
pauseButton = ttk.Button(controlBox, padding='2', text='Pause')
pauseButton.grid(column=0, row=0, sticky=(N, S, W))
pauseButton.columnconfigure(0, weight=1)
pauseButton.rowconfigure(0, weight=1)

#Button to start the crawler
goButton = ttk.Button(controlBox, padding='2', text='Go')
goButton.grid(column=1, row=0, sticky=(N, S))
goButton.columnconfigure(1, weight=1)
goButton.rowconfigure(0, weight=1)

#Button to stop the crawler
stopButton = ttk.Button(controlBox, padding='2', text='Stop')
stopButton.grid(column=2, row=0, sticky=(N, S, E))
stopButton.columnconfigure(2, weight=1)
stopButton.rowconfigure(0, weight=1)

ttk.Label(settingBox, text='Crawler Settings').grid(column=0, row=0, columnspan=3)

overwriteCheck = ttk.Checkbutton(settingBox, text='Overwrite', variable=Overwrite)
overwriteCheck.grid(column=0, row=1, sticky=(W))
overwriteCheck.columnconfigure(0, weight=1)
overwriteCheck.rowconfigure(1, weight=1)

raiseErrorsCheck = ttk.Checkbutton(settingBox, text='Raise Errors', variable=RaiseErrors)
raiseErrorsCheck.grid(column=0, row=2, sticky=(W))
raiseErrorsCheck.columnconfigure(0, weight=1)
raiseErrorsCheck.rowconfigure(2, weight=1)

savePagesCheck = ttk.Checkbutton(settingBox, text='Save Pages', variable=SavePages)
savePagesCheck.grid(column=0, row=3, sticky=(W))
savePagesCheck.columnconfigure(0, weight=1)
savePagesCheck.rowconfigure(3, weight=1)

zipFilesCheck = ttk.Checkbutton(settingBox, text='Zip Files', variable=ZipFiles)
zipFilesCheck.grid(column=0, row=4, sticky=(W))
zipFilesCheck.columnconfigure(0, weight=1)
zipFilesCheck.rowconfigure(4, weight=1)

saveWordsCheck = ttk.Checkbutton(settingBox, text='Save Words', variable=SaveWords)
saveWordsCheck.grid(column=0, row=5, sticky=(W))
saveWordsCheck.columnconfigure(0, weight=1)
saveWordsCheck.rowconfigure(5, weight=1)

saveCountEntry = ttk.Entry(settingBox, width=5, textvariable=SaveCount)
saveCountEntry.grid(column=0, row=6, sticky=(W))
saveCountEntry.columnconfigure(0, weight=1)
saveCountEntry.rowconfigure(6, weight=1)

getTodoFileButton = ttk.Button(settingBox, text='...', command=get_file)
getTodoFileButton.grid(column=1, row=1, sticky=())
getTodoFileButton.columnconfigure(1, weight=1)
getTodoFileButton.rowconfigure(1, weight=1)

ttk.Label(settingBox, text='TODO File').grid(column=2, row=1)

getDoneFileButton = ttk.Button(settingBox, text='...', command=get_file)

window.mainloop()
