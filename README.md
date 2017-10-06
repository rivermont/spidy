# spidy Web Crawler
Spidy (/spˈɪdi/) is the simple, easy to use command line web crawler.<br>
Given a list of web links, it uses the Python [`requests`](http://docs.python-requests.org) library to query the webpages.<br>
Spidy then uses [`lxml`](http://lxml.de/index.html) to extract all links from the page and adds them to its list.<br>
Pretty simple!

Started by [rivermont](https://github.com/rivermont) (/rɪvɜːrmɒnt/) and [FalconWarriorr](https://github.com/Casillas-) (/fælcʌnraɪjɔːr/).<br>
Looking for technical documentation? Check out [DOCS.md](https://github.com/rivermont/spidy/blob/master/DOCS.md)<br>
Looking to contribute to this project? Have a look at [`CONTRIBUTING.md`](https://github.com/rivermont/spidy/blob/master/CONTRIBUTING.md), then check out the docs.

![Version: 1.4.2](https://img.shields.io/badge/version-1.4.2-brightgreen.svg)
[![Release: 1.4.0](https://img.shields.io/github/release/rivermont/spidy.svg)](https://github.com/rivermont/spidy/releases)
[![License: GPL v3](https://img.shields.io/badge/license-GPLv3.0-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![Python 3.3+](https://img.shields.io/badge/python-3.3+-brightgreen.svg)](https://docs.python.org/3/)
![All Platforms!](https://img.shields.io/badge/Windows,%20OS/X,%20Linux-%20%20-brightgreen.svg)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)
<br>
![Lines of Code: 1321](https://img.shields.io/badge/lines%20of%20code-1321-brightgreen.svg)
![Lines of Docs: 559](https://img.shields.io/badge/lines%20of%20docs-559-green.svg)
[![Last Commit](https://img.shields.io/github/last-commit/rivermont/spidy.svg)](https://github.com/rivermont/spidy/graphs/punch-card)
[![Travis CI Status](https://img.shields.io/travis/rivermont/spidy/master.svg)](https://travis-ci.org/rivermont/spidy)
<br>
[![Contributors](https://img.shields.io/github/contributors/rivermont/spidy.svg)](https://github.com/rivermont/spidy/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/rivermont/spidy.svg?style=social&label=Forks)](https://github.com/rivermont/spidy/network)
[![Stars](https://img.shields.io/github/stars/rivermont/spidy.svg?style=social&label=Stars)](https://github.com/rivermont/spidy/stargazers)

***

# New Features!

### Automatic Testing with Travis CI

### Release v1.4.0 - #[31663d3](https://github.com/rivermont/spidy/commit/31663d34ceeba66ea9de9819b6da555492ed6a80)
[spidy Web Crawler Release 1.4](https://github.com/rivermont/spidy/releases/tag/1.4.0)

### Domain Limiting - #[e229b01](https://github.com/rivermont/spidy/commit/e229b01eed7e1f95530d06afc671e40dbf4dac53)
Scrape only a single site instead of the whole internet. May use slightly less space on your disk.<br>
See `config/wsj.cfg` for an example.

### Release v1.0!
[spidy Web Crawler Release 1.0](https://github.com/rivermont/spidy/releases/tag/1.0)


# Contents

  - [spidy Web Crawler](#spidy-web-crawler)
  - [New Features!](#new-features)
  - [Contents](#contents)
  - [How it Works](#how-it-works)
  - [Features](#features)
  - [Tutorial](#tutorial)
    - [Python Installation](#python-installation)
      - [Windows and Mac](#windows-and-mac)
        - [Anaconda](#anaconda)
        - [Python Base](#python-base)
      - [Linux](#linux)
    - [Crawler Installation](#crawler-installation)
    - [Launching](#launching)
    - [Running](#running)
      - [Config](#config)
      - [Start](#start)
      - [Autosave](#autosave)
      - [Force Quit](#force-quit)
  - [License](#license)


# How it Works
Spidy has two working lists, `TODO` and `DONE`.<br>
TODO is the list of URLs it hasn't yet visited.<br>
Done is the list of URLs it has already been to.<br>
The crawler visits each page in TODO, scrapes the DOM of the page for links, and adds those back into TODO.<br>
It can also save each page, because datahoarding 😜.


# Features
We built a lot of the functionality in spidy by watching the console scroll by and going, "Hey, we should add that!"<br>
Here are some features we figure are worth noting.

  - Error Handling: We have tried to recognize all of the errors spidy runs into and create custom error messages and logging for each. There is a set cap so that after accumulating too many errors the crawler will stop itself.
  - Cross-Platform compatability: spidy will work on all three major operatin systems, Windows, Mac OS/X, and Linux!
  - Frequent Timestamp Logging: Spidy logs almost every action it takes to both the console and one of two log files.
  - Browser Spoofing: Make requests using User Agents from 4 popular web browsers, use a custom spidy bot one, or create your own!
  - Portability: Move spidy's folder and its contents somewhere else and it will run right where it left off.
  - User-Friendly Logs: Both the console and log file messages are simple and easy to interpret, but packed with information.
  - Webpage saving: Spidy downloads each page that it runs into, regardless of file type. The crawler uses the HTTP `Content-Type` header returned with most files to determine the file type.
  - File Zipping: When autosaving, spidy can archive the contents of the `saved/` directory to a `.zip` file, and then clear `saved/`.


# Tutorial
The way that you will run spidy depends on the way you have Python installed.<br>
Spidy can be run from the command line (on Mac systems), a Python IDE, or (on Windows systems) by launching the `.bat` file.

## Python Installation

### Windows and Mac

There are many different versions of [Python](https://www.python.org/about/), and hundreds of different installations for each them.<br>
Spidy is developed for Python v3.5.2, but should run without errors in other versions of Python 3.

#### Anaconda
We recommend the [Anaconda distribution](https://www.continuum.io/downloads).<br>
It comes pre-packaged with lots of goodies, including `lxml`, which is required for spidy to run and not including in the standard Python package.

#### Python Base
You can also just install [default Python](https://www.python.org/downloads/), and install the external libraries separately.<br>
This can be done with `pip`:

    pip install -r requirements.txt

### Linux
Python 3 should come preinstalled with most flavors of Linux, but if not, simply run

    sudo apt update
    sudo apt install python3 python3-lxml python3-requests

Then `cd` into the crawler's directory and run `python3 crawler.py`.

## Crawler Installation
If you have git or GitHub Desktop installed, you can clone the repository [from here](https://github.com/rivermont/spidy.git). If not, download [the latest source code](https://github.com/rivermont/spidy/archive/master.zip) or grab the [latest release](https://github.com/rivermont/spidy/releases).

### Launching

Use `cd` to navigate to the directory that spidy is located in, then run:

    python crawler.py

![](/media/run.gif?raw=true)

### Running
Spidy logs a lot of information to the command line throughout its life.<br>
Once started, a bunch of `[INIT]` lines will print.<br>
These announce where spidy is in its initialization process.<br>

#### Config
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


# License
We used the [Gnu General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html) (see [LICENSE](https://github.com/rivermont/spidy/blob/master/LICENSE)) as it was the license that best suited our needs.<br>
Honestly, if you link to this repo and credit `rivermont` and `FalconWarriorr`, and you aren't selling spidy in any way, then we would love for you to distribute it.<br>
Thanks!

***
