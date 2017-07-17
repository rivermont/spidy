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
from os import  path
DIR = path.dirname(path.realpath(__file__))
#from crawler import main

#crawlerThread = Thread(target = main)

#def runCrawler():
#    crawlerThread.start()

def get_file():
	return filedialog.askopenfilename()

def get_text(field):
	return field.get('1.0', 'end')

#Main window
window = Tk()
window.title('spidy Web Crawler - by rivermont')
window.iconbitmap('{0}\\media\\favicon.ico'.format(DIR))

#Frame to fill main window
mainFrame = ttk.Frame(window, padding='5')
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
MaxNewErrors = IntVar()
MaxHTTPErrors = IntVar()
MaxKnownErrors = IntVar()
MaxNewMIMEs = IntVar()
CustomHeaders = StringVar()

#Container to hold variable settings
settingBox = ttk.Frame(mainFrame, padding='5', borderwidth=1, relief='solid')
settingBox.grid(column=0, row=0, sticky=(N, S, W))
settingBox.columnconfigure(0, weight=1)
settingBox.rowconfigure(0, weight=1)

#Container for things on the right side of the main window
rightBar = ttk.Frame(mainFrame, padding='5', borderwidth=1, relief='solid')
rightBar.grid(column=1, row=0, sticky=(N, S, E))
rightBar.columnconfigure(2, weight=1)
rightBar.rowconfigure(0, weight=1)

#Container for controlling the crawler
controlBox = ttk.Frame(rightBar, padding='5', borderwidth=1, relief='solid')
controlBox.grid(column=1, row=0, sticky=(N, E, W))
controlBox.columnconfigure(1, weight=1)
controlBox.rowconfigure(0, weight=1)

#Container for the status elements
statusBox = ttk.Frame(rightBar, padding='5', borderwidth=1, relief='solid')
statusBox.grid(column=0, row=1, sticky=(E, W))
statusBox.columnconfigure(0, weight=1)
statusBox.rowconfigure(1, weight=1)

#Container for the console log
consoleBox = ttk.Frame(rightBar, padding='5', borderwidth=1, relief='solid')
consoleBox.grid(column=0, row=2)
consoleBox.columnconfigure(0, weight=1)
consoleBox.rowconfigure(2, weight=1)

#Button to pause the crawler
pauseButton = ttk.Button(controlBox, padding='5', text='Pause')
pauseButton.grid(column=0, row=0, sticky=(N, S, W))
pauseButton.columnconfigure(0, weight=1)
pauseButton.rowconfigure(0, weight=1)

#Button to start the crawler
goButton = ttk.Button(controlBox, padding='5', text='Go')
goButton.grid(column=1, row=0, sticky=(N, S))
goButton.columnconfigure(1, weight=1)
goButton.rowconfigure(0, weight=1)

#Button to stop the crawler
stopButton = ttk.Button(controlBox, padding='5', text='Stop')
stopButton.grid(column=2, row=0, sticky=(N, S, E))
stopButton.columnconfigure(2, weight=1)
stopButton.rowconfigure(0, weight=1)

#Title for crawler setting area
ttk.Label(settingBox, text='Crawler Settings', padding='5').grid(column=0, row=0, columnspan=4, sticky=(N ,S))

#Option to set Overwrite
overwriteCheck = ttk.Checkbutton(settingBox, text='Overwrite', variable=Overwrite, padding='5')
overwriteCheck.grid(column=0, row=1, columnspan=2, sticky=(W))
overwriteCheck.columnconfigure(0, weight=1)
overwriteCheck.rowconfigure(1, weight=1)

#Option to set RaiseErrors
raiseErrorsCheck = ttk.Checkbutton(settingBox, text='Raise Errors', variable=RaiseErrors, padding='5')
raiseErrorsCheck.grid(column=0, row=2, columnspan=2, sticky=(W))
raiseErrorsCheck.columnconfigure(0, weight=1)
raiseErrorsCheck.rowconfigure(2, weight=1)

#Option to set SavePages
savePagesCheck = ttk.Checkbutton(settingBox, text='Save Pages', variable=SavePages, padding='5')
savePagesCheck.grid(column=0, row=3, columnspan=2, sticky=(W))
savePagesCheck.columnconfigure(0, weight=1)
savePagesCheck.rowconfigure(3, weight=1)

#Option to set ZipFiles
zipFilesCheck = ttk.Checkbutton(settingBox, text='Zip Files', variable=ZipFiles, padding='5')
zipFilesCheck.grid(column=0, row=4, columnspan=2, sticky=(W))
zipFilesCheck.columnconfigure(0, weight=1)
zipFilesCheck.rowconfigure(4, weight=1)

#Option to set SaveWords
saveWordsCheck = ttk.Checkbutton(settingBox, text='Save Words', variable=SaveWords, padding='5')
saveWordsCheck.grid(column=0, row=5, columnspan=2, sticky=(W))
saveWordsCheck.columnconfigure(0, weight=1)
saveWordsCheck.rowconfigure(5, weight=1)

#Field to enter number for SaveCount
ttk.Label(settingBox, text='Save Count').grid(column=0, row=6, columnspan=2, sticky=(W))

saveCountEntry = ttk.Entry(settingBox, width=5, textvariable=SaveCount)
saveCountEntry.grid(column=0, row=7, sticky=(E, W))
saveCountEntry.columnconfigure(0, weight=1)
saveCountEntry.rowconfigure(7, weight=1)

#Field to enter custom headers
ttk.Label(settingBox, text='Custom Headers').grid(column=0, row=8, columnspan=2, sticky=(W))

customHeadersEntry = Text(settingBox, height=3, width=16)
customHeadersEntry.grid(column=0, row=9, columnspan=2, sticky=(W))
customHeadersEntry.columnconfigure(0, weight=1)
customHeadersEntry.rowconfigure(9, weight=1)

#Field to enter custom starting links
ttk.Label(settingBox, text='Start Links').grid(column=0, row=10, columnspan=2, sticky=(W))

customStartLinks = Text(settingBox, height=2, width=16)
customStartLinks.grid(column=0, row=11, columnspan=2, sticky=(W))
customStartLinks.columnconfigure(0, weight=1)
customStartLinks.rowconfigure(11, weight=1)

#Button to select todo file
getTodoFileButton = ttk.Button(settingBox, text='...', command=get_file)
getTodoFileButton.grid(column=2, row=1, sticky=(W))
getTodoFileButton.columnconfigure(1, weight=1)
getTodoFileButton.rowconfigure(2, weight=1)

ttk.Label(settingBox, text='TODO File').grid(column=3, row=1, sticky=(W))

#Button to select done file
getDoneFileButton = ttk.Button(settingBox, text='...', command=get_file)
getDoneFileButton.grid(column=2, row=2, sticky=(W))
getDoneFileButton.columnconfigure(2, weight=1)
getDoneFileButton.rowconfigure(2, weight=1)

ttk.Label(settingBox, text='Done File').grid(column=3, row=2, sticky=(W))

#Button to select bad link file
getBadFileButton = ttk.Button(settingBox, text='...', command=get_file)
getBadFileButton.grid(column=2, row=3, sticky=(W))
getBadFileButton.columnconfigure(2, weight=1)
getBadFileButton.rowconfigure(3, weight=1)

ttk.Label(settingBox, text='Bad Link File').grid(column=3, row=3, sticky=(W))

#Button to select word file
getWordFileButton = ttk.Button(settingBox, text='...', command=get_file)
getWordFileButton.grid(column=2, row=4, sticky=(W))
getWordFileButton.columnconfigure(2, weight=1)
getWordFileButton.rowconfigure(4, weight=1)

ttk.Label(settingBox, text='Word File').grid(column=3, row=4, sticky=(W))

#Field to set MaxNewErrors
maxNewErrorEntry = ttk.Entry(settingBox, width=4, textvariable=MaxNewErrors)
maxNewErrorEntry.grid(column=2, row=5, sticky=(E, W))
maxNewErrorEntry.columnconfigure(2, weight=1)
maxNewErrorEntry.rowconfigure(5, weight=1)

ttk.Label(settingBox, text='Max New Errors').grid(column=3, row=5, sticky=(W))

#Field to set MaxHTTPErrors
maxHTTPErrorEntry = ttk.Entry(settingBox, width=4, textvariable=MaxHTTPErrors)
maxHTTPErrorEntry.grid(column=2, row=6, sticky=(E, W))
maxHTTPErrorEntry.columnconfigure(2, weight=1)
maxHTTPErrorEntry.rowconfigure(6, weight=1)

ttk.Label(settingBox, text='Max HTTP Errors').grid(column=3, row=6, sticky=(W))

#Field to set MaxKnownErrors
maxKnownErrorsEntry = ttk.Entry(settingBox, width=4, textvariable=MaxKnownErrors)
maxKnownErrorsEntry.grid(column=2, row=7, sticky=(E, W))
maxKnownErrorsEntry.columnconfigure(2, weight=1)
maxKnownErrorsEntry.rowconfigure(7, weight=1)

ttk.Label(settingBox, text='Max Known Errors').grid(column=3, row=7, sticky=(W))

#Field to set MaxNewMIMEs
maxNewMIMEsEntry = ttk.Entry(settingBox, width=4, textvariable=MaxNewMIMEs)
maxNewMIMEsEntry.grid(column=2, row=8, sticky=(E, W))
maxNewMIMEsEntry.columnconfigure(2, weight=1)
maxNewMIMEsEntry.rowconfigure(8, weight=1)

ttk.Label(settingBox, text='Max New MIMEs').grid(column=3, row=8, sticky=(W))

window.mainloop()
