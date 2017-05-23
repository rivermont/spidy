# spidy
Spidy (spˈɪdi) is the simple, easy to use command line web crawler.
Given a list of web links, it uses the Python lxml and requests libraries to query the webpages.
Spidy then extracts all links from the DOM of the page and adds them to its list.

--------------------

# Table of Contents

  - [How it Works](#how-it-works)
  - [Features](#features)
    - [Error Handling](#error-handling)
    - [Frequent Timestamp Logging](frequent-timestamp-logging)
    - [Startup](#startup)
    - [User-Friendly Logs](#user-friendly-logs)
  - [Tutorial](#tutorial)
    - [Python Installation](#python-installation)
    - [Launching](#launching)
      - [Command Arguments](#command-arguments)
      - [Windows (Command Line)](#windows-command-line)
      - [Windows (batch file)](#windows-batch-file)
      - [Linux Command Line](#linux-command-line)
      - [OS X Command Line](#os-x-command-line)
    - [Running](#running)
  - [Files](#files)
    - [README.md](#readmemd)
    - [clear.bat](#clearbat)
    - [crawler.py](#crawlerpy)
    - [errors.txt](#errorstxt)
    - [makefiles.bat](#makefilesbat)
    - [post-process.py](#post-processpy)
    - [run.bat](#runbat)
  - [Branches](#the-branches)
    - [master](#master)
	- [FalconWarriorr-branch](#falconwarriorr-branch)
  - [Acknowledgements](#acknoowledgements)

# How it Works
Spidy has to working lists, `TODO` and `done`.
TODO is the list of URLs it hasn't yet visited.
Done is the list of URLs it has already been to.
The crawler visits each page in TODO, scrapes the html content for links, and adds those back into TODO.
It also saves all of the content of the page into a file for processing.


# Features
We built a lot of the functionality in spidy by watching the console scroll by and going, "Hey, we should add that!"
Here are some features that we think are worth noting, in alphabetic order.

## Error Handling
While testing we have come across many common errors that aren't easily avoided such as http timeout, unicode encode errors, exceeding maximum redirects, http connection, and document empty(going to picture etc.)
For all of these errors we have separate error handling that prints a relevant sttatement to the console since most of these errors are impossible to avoid we just continue past them.
For unknown errors we have a cap which will cause the program to stop if we exceed that set amount.
Currently Spidy has built-in support for

 - UnicodeEncodeError
 - SSLError
 - XMLSyntaxError, ParserError
 - TooManyRedirects
 - ConnectionError
 - ContentDecodingError

## Frequent Timestamp Logging
Spidy logs almost every action it takes to both the command console and the logFile.

## User-Friendly Logs
Both the console and logFile messages are simple and easy to interpret, but packed with information.


# Tutorial
The way that you will run spidy depends on the way you have Python installed.
Spidy can be run from the command line, a Python IDE or (on Windows systems) by launching the .bat file.

![](/media/run.png?raw=true)

## Python Installation
There are many different versions of Python, and probably hundreds of different installations of each them.
Spidy is developed in Python v3.6.1, but should run without errors in other versions of Python 3.
rivermont is using Python installed through the [Anaconda distribution](https://www.continuum.io/downloads), and Falconwarriorr uses [Python's standard distro](https://www.python.org/downloads/).

## Launching

### Command Arguments
Spidy has 6 different command line arguments that control the behaviour of the crawler.
Because of the way it's written, args are optional but you must do them in a set order.
You can do `1, 2, 3`, but not `1, 3, 4`.

> python crawler.py [overwrite] [raiseErrors] [todoFile] [doneFile] [logFile] [wordFile] [saveCount]

The defaults are `False`, `False`, `crawler_todo.txt`, `crawler_done.txt`, `crawler_log`, `crawler_words.txt`, `100`.

 - overwrite (Bool): Whether to load from the save files or not. Spidy will always save to the save files.
 - raiseErrors (Bool): Whether to stop the script when an error occurs that it can;t handle by default.
 - todoFile (str): The location of the TODO file. Spidy will load from and save to this file..
 - doneFile (str): The location of the done file. Spidy will load from and save to this file.
 - logFile (str): The location of the log file. Spidy will save to this file, apppending logs to the end.
 - saveCount (int): The number of processed links after which to autosave.

### Windows (Command Line)
Use cd to navigate to the spidy's directory located in, then run the `makefiles.bat`.
This will create all of the neccessary files if they don't already exist.

> python crawler.py True False crawler_todo.txt crawler_done.txt crawler_log.txt 100

### Windows (batch file)
Use cd to navigate to spidy's directory and run the `makefiles.bat`.
This will create all of the neccessary files if they don't already exist.
Then run `run.bat`.

![options example](/media/bat.png?raw=true "options pic")

In the .bat file that runs the web-crawler.py you can specify arguments to control the behavior of the crawler the first argument after specifying the python script is todo file where you can specify a separate file if you want to save multiple to do lists or already have a preset one default is crawler_todo.txt.
Second argument is done file where same as to do you can specify a specific file where you want to load a done list from or save to default is crawler_done.txt.
Third argument is log file where you can specify a file where you want so write all error messages etc to default is crawler_log.txt.
Fourth argument is after how many queried webpages will the crawler autosave todo and done lists(default is 1000 iterations.

### Linux Command Line
Do things.

### OS X Command Line
Do things.

## Running

![](/media/run.mp4?raw=true "running gif")

Spidy logs a lot of information to the command line.
Once started, a bunch of `[INIT]` lines will print.
These announce where spidy is in its initialization process.
If it takes a long time on `[INIT]: Pruning invalid links from TODO...`, that's fine - it has to process every link in the TODO list, which can be hundreds of thousands of lines long.

![Start example](/media/start.png?raw=true "Start pic")


# Files
Detailing each important file.

## README.md
This readme file.

## clear.bat
Clears all save files by deleting them and creating empty ones.

## crawler.py
The important code. This is what you will run to crawl links and save information.
Because the internet is so big, this will practically never end.

## errors.txt
A log of all the errors we encounter, sorted by frequency.
This is used to improve the efficiency of the error handling.

## makefiles.bat
Creates all of the needed save files for spidy to run.

## post-process.py
This removes all the lines in `crawler_words.txt` longer than 16 characters.
Run this after running crawler.py for a while.

## run.bat
A Windows batch file to run the program.
Theoretically once the crawler finishes running post-process with run, but you'd have to get the entire internet first, so...


# Branches
Detailing each active branch of the project.

## master
The stable, up-to-date branch.

## FalconWarriorr-branch
Falconwarriorr's development branch.
He is constantly adding new features to his, and I am slowly implementing them into the master branch.


# Acknowledgements
I'd like to thank Pluralsight for providing an amazing platfom for learning any language.
Specifically the Python Fundamentals course by Austin Bingham and Robert Smallshire.
