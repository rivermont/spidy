# web-crawler
A simple to use command line web crawler that saves all visited website links to a folder along with all valid archived links

# how it works
This web crawler is very simple in that the main functionality is it's ability to parse the html for all links and then adds all of those links that are valid into a list called todo. As you would expect the crawler then goes on to do this same process for all links in todo. After every  1000 links queried (by default) the crawler will autosave the done file and will prune the links for any invalid ones.

## Python Installation
There are many different versions of Python, and probably hundreds of different installations of each them.
Spidy is developed in Python v3.6.1, but should run without errors in other versions of Python 3, but you will need a scientific distribution of python for lxml to run without errors. Downloading anaconda is a great way to get all the python functionality that 
need along with an ide and the ability to compile and run from the command line.

## How to use
For this version of spidy all you have to do to run this is make sure that you have a log file, todo file, done file, and text file, that are either named (crawler_log.txt, crawler_done.txt, crawler_todo.txt, and crawler_text.txt) or anything else that you want as long as you type y when asked if you want to change default save settings. To actually run spidy from the command line with anaconda installed all you need to do is make sure you are in the correct directory with python script in it. Just type python site-test.py and you are off or if you are on a windows system just run the .bat file to run it for you.

# startup
User friendly log messages are printed in the console letting you know what proccess is going an if it is taking a long time and you don't know why. Before it starts crawling it will ask you whether you want to change the default save settings which if you just have the default crawler_done.txt etc... you shoudl type n or anything else and press enter. If however you would like to save everything to separate files you should type y and press enter. Please note that this script will not create those files so make sure the files you specify already exist. Next you will be asked if you want to clear done file if this is your first time just press enter or type True if you want it to clear done. Next it will ask you whether you want to clear to do. Same as before type anything or press enter to do nothing or type True if you would like to clear it. Lastly it will ask the same for the text file. These options are especially useful if you had just run the crawler since the todo and text files grow especially large and sometimes takes a really long time to load.
![Start example](/Start.png?raw=true "Start pic")

# keyboard shortcuts
In this version of spidy you have the ability to press a multitude of keys while the program is running to pause, update files, get status, prune todo, and restart the crawling process. While it is running if you would like to pause the process you can press the p key and it will pause and give this dialog
![Pause example](/pause.png?raw=true "Pause pic")

In the pause menu, and while the program is normally running you can press u, r, e, and s to update, restart, prune todo, and get status respectively. During the pause menu you will have to press enter afterwards but during the normal program run you won't have to. All of these commands are visible while the program is running at the bottom of the command line so that you always know what commands you have access to.
![Keyboard example](/keyboard.png?raw=true "Keyboard pic")

# error handling and management
While testing we have come across many common errors that aren't easily avoided such as http timeout, unicode encode errors, exceeding maximum redirects, http connection, and document empty(going to picture etc.) For all of these errors we have separate error handling that prints a relevant sttatement to the console since most of these errors are impossible to avoid we just continue past them. For unknown errors we have a cap which will cause the program to stop if we exceed that set amount.

# Log files
All errors are logged to a log file that is by default crawler_log.txt but can be specified at startup. These error messages are all marked by a time stamp so if you walk away you will know exactly when any errors occurred. In addition any autosaves are also logged to this file to let you know how much data was lost if the program crashed for any reason. 
