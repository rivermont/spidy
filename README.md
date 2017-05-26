# spidy
Spidy (spˈɪdi) is the simple, easy to use command line web crawler.
Given a list of web links, it uses the Python [`lxml`](http://lxml.de/index.html) and `requests` libraries to query the webpages.
Spidy then extracts all links from the DOM of the page and adds them to its list.
It does this to infinity.[*](#asterisk)

[![License: GPL v3](https://img.shields.io/badge/license-GPLv3.0-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![Python: 3.6](https://img.shields.io/badge/python-3.6-brightgreen.svg)](https://docs.python.org/3/)
[![Python: 3](https://img.shields.io/badge/python-3-lightgrey.svg)](https://docs.python.org/3/)

--------------------

# Table of Contents

  - [spidy](#spidy)
  - [Table of Contents](#table-of-contents)
  - [How it Works](#how-it-works)
  - [Features](#features)
    - [Error Handling](#error-handling)
    - [Frequent Timestamp Logging](#frequent-timestamp-logging)
    - [User-Friendly Logs](#user-friendly-logs)
  - [Tutorial](#tutorial)
    - [Python Installation](#python-installation)
      - [Anaconda](#anaconda)
      - [Python Base](#python-base)
    - [Launching](#launching)
      - [Command Arguments](#command-arguments)
      - [Windows (Command Line)](#windows-command-line)
      - [Windows (batch file)](#windows-batch-file)
    - [Running](#running)
	  - [Start](#start)
	  - [Autosave](#autosave)
	  - [Force Quit](#fore-quit)
	  - [End](#end)
  - [Files](#files)
    - [media/](#media)
	- [data/](#data)
    - [README.md](#readmemd)
    - [clear.bat](#clearbat)
    - [crawler.py](#crawlerpy)
    - [errors.txt](#errorstxt)
    - [makefiles.bat](#makefilesbat)
    - [post-process.py](#post-processpy)
    - [run.bat](#runbat)
  - [Branches](#branches)
    - [master](#master)
	- [FalconWarriorr-branch](#falconwarriorr-branch)
	- [saving-test](#saving-test)
	- [timings](#timings)
	- [verbose](#verbose)
  - [TODO](#todo)
  - [Acknowledgements](#acknowledgements)
  - [Contribute](#contribute)
  - [License](#license)

# How it Works
Spidy has to working lists, `TODO` and `done`.
TODO is the list of URLs it hasn't yet visited.
Done is the list of URLs it has already been to.
The crawler visits each page in TODO, scrapes the HTML content for links, and adds those back into TODO.
It also saves all of the content of the page into a file for processing.


# Features
We built a lot of the functionality in spidy by watching the console scroll by and going, "Hey, we should add that!"
Here are some features we figure are worth noting.

## Error Handling
We have tried to recognize all of the errors spidy runs into and create custom error messages and logging for each.
There is a set cap so that after accumulating too many errors the crawler will stop itself.
Currently Spidy has built-in support for

  - ConnectionError
  - UnicodeEncodeError
  - SSLError
  - XMLSyntaxError, ParserError
  - TooManyRedirects
  - ContentDecodingError
  - OSError

## Frequent Timestamp Logging
Spidy logs almost every action it takes to both the command console and the logFile.

## User-Friendly Logs
Both the console and logFile messages are simple and easy to interpret, but packed with information.


# Tutorial
The way that you will run spidy depends on the way you have Python installed.
Spidy can be run from the command line, a Python IDE, or (on Windows systems) by launching the .bat file.

## Python Installation
There are many different versions of [Python](https://www.python.org/about/), and probably hundreds of different installations of each them.
Spidy is developed in Python v3.6.1, but should run without errors in other versions of Python 3.

### Anaconda
We recommend the [Anaconda distribution](https://www.continuum.io/downloads).
It comes pre-packaged with lots of goodies, including `lxml`, which is required for spidy to run and not including in the standard Python distro.

### Python Base
If you do choose to go with the [default Python](https://www.python.org/downloads/) distribution, you will need to install the `lxml` library for spidy to work.
This can be done with `pip`:

> pip install lxml

## Launching

![](/media/run.gif?raw=true)

### Command Arguments
Spidy has 6 different command line arguments that control the behavior of the crawler.
Because of the way it's written, args are optional but you must do them in a set order.
You can do `1, 2, 3`, but not `1, 3, 4`.

> python crawler.py [overwrite] [raiseErrors] [todoFile] [doneFile] [logFile] [wordFile] [saveCount]

The defaults are `False`, `False`, `crawler_todo.txt`, `crawler_done.txt`, `crawler_log`, `crawler_words.txt`, `100`.

 - overwrite (Bool): Whether to load from the save files or not. Spidy will always save to the save files.
 - raiseErrors (Bool): Whether to stop the script when an error occurs that it can;t handle by default.
 - todoFile (str): The location of the TODO file. Spidy will load from and save to this file.
 - doneFile (str): The location of the done file. Spidy will load from and save to this file.
 - logFile (str): The location of the log file. Spidy will save to this file, apppending logs to the end.
 - wordFile (str): The location of the words file. Spidy will load from and save to this file.
 - saveCount (int): The number of processed links after which to autosave.

### Windows (Command Line)
Use `cd` to navigate to the directory spidy's located in, then run the `makefiles.bat`.
This will create all of the necessary files if they don't already exist.

> python crawler.py True False crawler_todo.txt crawler_done.txt crawler_log.txt 100

### Windows (batch file)
Use `cd` to navigate to spidy's directory and run the `makefiles.bat`.
This will create all of the necessary files if they don't already exist.
Then run `run.bat`.

## Running
Spidy logs a lot of information to the command line.
Once started, a bunch of `[INIT]` lines will print.
These announce where spidy is in its initialization process.
If it takes a long time on `[INIT]: Pruning invalid links from TODO...`, that's fine - it has to process every link in the TODO list, which can be hundreds of thousands of lines long.

### Start
Sample start log.

![](/media/start.png?raw=true)

### Autosave
Sample log after hitting the autosave cap.

![](/media/log.png?raw=true)

### Force Quit
Sample log after performing a `^C` to force quit the crawler.

![](/media/keyboardinterrupt.png?raw=true)

### End
Sample log after crawler visits all links in TODO.

![](/media/end.png?raw=true)


# Files

## media/
Images used in this readme file.

## data/
Post-processed wordlists.

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

## master
The stable, up-to-date branch.

## FalconWarriorr-branch
Falconwarriorr's development branch.
He is constantly adding new features to his, and I am slowly implementing them into the master branch.

## saving-test
The old development branch for implementing word saving.

## timings
The old development branch for adding timestamps to all the logs.

## verbose
The old development branch for implementing logging.


# TODO
  - Upload spidy to PyPI
  - Log length of wordFile to logFile
  - Log saving of webpage to console.
  - Add webpage saving functionality to README
  - Talk about hashcat in README

# Acknowledgements
I'd like to thank [Pluralsight](https://www.pluralsight.com/) for providing an amazing platform for learning any language.
Specifically the [Python Fundamentals](https://www.pluralsight.com/courses/python-fundamentals/) course by Austin Bingham and Robert Smallshire.


# Contribute
We would love your help with anything!
Right now neither of us have access to a Linux or OS/X machine, so we don't have any documentation for running spidy on those systems.
If you find a bug raise an issue, and if you have a suggestion go ahead and fork it.
We will happily look at anything that you build off of spidy; we're not very creative people and we know that there're more ideas out there!


# License
We used the [Gnu General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html) (see [LICENSE](https://github.com/rivermont/spidy/blob/master/LICENSE)) as it was the license that best suited our needs.
Honestly, if you link to this repo and credit `rivermont` and `Falconwarriorr`, and you aren't selling spidy in any way, then we would love for you to distribute it.
Thanks!


--------------------

### Asterisk
Studies have shown that the spidy web crawler will run to infinity, however it has not yet been proven whether there is computing power *beyond* infinity.
If there is, then yes - spidy will run to infinity **and bey**-
![](/media/physics.dll.png?raw=true)
