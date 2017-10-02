# spidy Web Crawler
Spidy (/spˈɪdi/) is the simple, easy to use command line web crawler.<br>
Given a list of web links, it uses the Python [`requests`](http://docs.python-requests.org) library to query the webpages.<br>
Spidy then uses [`lxml`](http://lxml.de/index.html) to extract all links from the page and adds them to its list.<br>
Pretty simple!

Developed by [rivermont](https://github.com/rivermont) (/rɪvɜːrmɒnt/) and [FalconWarriorr](https://github.com/Casillas-) (/fælcʌnraɪjɔːr/).<br>
Looking for technical documentation? Check out [docs.md](https://github.com/rivermont/spidy/blob/master/docs.md)<br>
Looking to contribute to this project? Have a look at [`CONTRIBUTING.md`](https://github.com/rivermont/spidy/blob/master/CONTRIBUTING.md), then check out the docs.

![Version: 1.3.1](https://img.shields.io/badge/version-1.3.1-brightgreen.svg)
[![Release: 1.3.0](https://img.shields.io/badge/release-1.3.0-brightgreen.svg)](https://github.com/rivermont/spidy/releases)
[![License: GPL v3](https://img.shields.io/badge/license-GPLv3.0-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![Python: 3.5](https://img.shields.io/badge/python-3.5-brightgreen.svg)](https://docs.python.org/3/)
[![Python: 3](https://img.shields.io/badge/python-3-lightgrey.svg)](https://docs.python.org/3/)
![Windows](https://img.shields.io/badge/Windows-%20%20-brightgreen.svg)
![Linux, OS/X](https://img.shields.io/badge/Linux,%20OS/X-%20%20-red.svg)
<br>
![Lines of Code: 1168](https://img.shields.io/badge/lines%20of%20code-1168-green.svg)
![Lines of Docs: 460](https://img.shields.io/badge/lines%20of%20docs-460-orange.svg)

--------------------

# New Features!

### Domain Limiting - #[e229b01](https://github.com/rivermont/spidy/commit/e229b01eed7e1f95530d06afc671e40dbf4dac53)
Scrape only a single site instead of the whole internet. May use slightly less space on your disk.<br>
See `config/wsj.cfg` for an example.

### Release v1.0!
[spidy Web Crawler Release 1.0](https://github.com/rivermont/spidy/releases/tag/1.0)

### PEP 8 Compliance - #[133dcdc](https://github.com/rivermont/spidy/commit/133dcdc02a0d63d94725cb86c089b7fdb3eba2d4)
98% of code now obeys the PEP 8 standard.<br>
[PEP 8](https://www.python.org/dev/peps/pep-0008/) is the Style Guide for all Python code.

### Better File Saving - #[8c0dcd4](https://github.com/rivermont/spidy/commit/8c0dcd4d637eadde4326065cbed74eafcb381dbe)
Now uses the `Content-Type` header to determine how to save files.<br>
Also cut the number of requests to sites in half, effectively killing HTTP 429 Errors.

# Table of Contents

  - [spidy](#spidy-web-crawler)
  - [New Features!](#new-features)
  - [Table of Contents](#table-of-contents)
  - [How it Works](#how-it-works)
  - [Features](#features)
  - [Tutorial](#tutorial)
    - [Windows and Mac](#windows)
      - [Python Installation](#python-installation)
        - [Anaconda](#anaconda)
        - [Python Base](#python-base)
      - [Launching](#launching)
        - [Command Line](#command-line)
    - [Running](#running)
      - [Config](#config)
      - [Start](#start)
      - [Autosave](#autosave)
      - [Force Quit](#force-quit)
      - [End](#end)
  - [License](#license)


# How it Works
Spidy has two working lists, `TODO` and `done`.<br>
TODO is the list of URLs it hasn't yet visited.<br>
Done is the list of URLs it has already been to.<br>
The crawler visits each page in TODO, scrapes the DOM of the page for links, and adds those back into TODO.<br>
It can also save each page, because datahoarding 😜.


# Features
We built a lot of the functionality in spidy by watching the console scroll by and going, "Hey, we should add that!"<br>
Here are some features we figure are worth noting.

  - Error Handling: We have tried to recognize all of the errors spidy runs into and create custom error messages and logging for each. There is a set cap so that after accumulating too many errors the crawler will stop itself.
  - Frequent Timestamp Logging: Spidy logs almost every action it takes to both the console and one of two log files.
  -  Portability: Move spidy's folder and its contents somewhere else and it will run right where it left off.
  - User-Friendly Logs: Both the console and log file messages are simple and easy to interpret, but packed with information.
  - Webpage saving: Spidy downloads each page that it runs into, regardless of file type. The crawler uses the HTTP `Content-Type` header returned with most files to determine the file type.
  - File Zipping: When autosaving, spidy can archive the contents of the `saved/` directory to a `.zip` file, and then clear `saved/`.


# Tutorial
The way that you will run spidy depends on the way you have Python installed.<br>
Spidy can be run from the command line (on Mac systems), a Python IDE, or (on Windows systems) by launching the `.bat` file.

## Windows and Mac

### Python Installation
There are many different versions of [Python](https://www.python.org/about/), and hundreds of different installations for each them.<br>
Spidy is developed for Python v3.5.2, but should run without errors in other versions of Python 3.

#### Anaconda
We recommend the [Anaconda distribution](https://www.continuum.io/downloads).<br>
It comes pre-packaged with lots of goodies, including `lxml`, which is required for spidy to run and not including in the standard Python package.

#### Python Base
You can also just install [default Python](https://www.python.org/downloads/), and install `lxml` separately.<br>
This can be done with `pip`:

> pip install lxml

### Launching

![](/media/run.gif?raw=true)

#### Command Line
Use `cd` to navigate to the directory that spidy is located in, then run:

> python crawler.py

## Running
Spidy logs a lot of information to the command line throughout its life.<br>
Once started, a bunch of `[INIT]` lines will print.<br>
These announce where spidy is in its initialization process.<br>

### Config
On running, spidy asks for input regarding certain parameters it will run off of.<br>
However, you can also use one of the configuration files, or even create your own.

To use spidy with a configuration file, input the name of the file when the crawler asks

The config files included with spidy are:

  - *`blank.txt`*: Template for creating your own configurations.
  - `default.cfg`: The default version.
  - `heavy.cfg`: Run spidy with all of its features enabled.
  - `infinite.cfg`: The default config, but it never stops itself.
  - `light.cfg`: Disable most features; only crawls pages for links.
  - `rivermont.cfg`: My personal favorite settings.
  - `rivermont-infinite.cfg`: My favorite, never-ending configuration.

### Start
Sample start log.

![](/media/start.png?raw=true)

### Autosave
Sample log after hitting the autosave cap.

![](/media/log.png?raw=true)

### Force Quit
Sample log after performing a `^C` (CONTROL + C) to force quit the crawler.

![](/media/keyboardinterrupt.png?raw=true)

### End
Sample log after crawler visits all links in TODO.

![](/media/end.png?raw=true)



# License
We used the [Gnu General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html) (see [LICENSE.md](https://github.com/rivermont/spidy/blob/master/LICENSE)) as it was the license that best suited our needs.<br>
Honestly, if you link to this repo and credit `rivermont` and `FalconWarriorr`, and you aren't selling spidy in any way, then we would love for you to distribute it.<br>
Thanks!

--------------------
