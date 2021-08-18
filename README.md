# spidy Web Crawler [![Mentioned in awesome-crawler](https://awesome.re/mentioned-badge.svg)](https://github.com/BruceDone/awesome-crawler)

Spidy (/spˈɪdi/) is the simple, easy to use command line web crawler.<br>
Given a list of web links, it uses Python [`requests`](http://docs.python-requests.org) to query the webpages, and [`lxml`](http://lxml.de/index.html) to extract all links from the page.<br>
Pretty simple!

[![spidy Logo](https://raw.githubusercontent.com/rivermont/spidy/master/media/spidy_logo.png)](https://github.com/rivermont/spidy#contributors)

![Version: 1.6.5](https://img.shields.io/badge/version-1.6.5-brightgreen.svg)
[![Release: 1.4.0](https://img.shields.io/github/release/rivermont/spidy.svg)](https://github.com/rivermont/spidy/releases)
[![License: GPL v3](https://img.shields.io/badge/license-GPLv3.0-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![Python 3.3+](https://img.shields.io/badge/python-3.3+-brightgreen.svg)](https://docs.python.org/3/)
![All Platforms!](https://img.shields.io/badge/Windows,%20OS/X,%20Linux-%20%20-brightgreen.svg)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)
<br>
![Lines of Code: 1553](https://img.shields.io/badge/lines%20of%20code-1553-brightgreen.svg)
![Lines of Docs: 605](https://img.shields.io/badge/lines%20of%20docs-605-orange.svg)
[![Last Commit](https://img.shields.io/github/last-commit/rivermont/spidy.svg)](https://github.com/rivermont/spidy/graphs/punch-card)
[![Travis CI Status](https://img.shields.io/travis/com/rivermont/spidy)](https://travis-ci.com/github/rivermont/spidy)
[![PyPI Wheel](https://img.shields.io/pypi/wheel/spidy-web-crawler.svg)](https://pypi.org/project/spidy-web-crawler/)
[![PyPI Status](https://img.shields.io/pypi/status/spidy-web-crawler.svg)](https://pypi.org/project/spidy-web-crawler/)
<br>
[![Contributors](https://img.shields.io/github/contributors/rivermont/spidy.svg)](https://github.com/rivermont/spidy/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/rivermont/spidy.svg?style=social&label=Forks)](https://github.com/rivermont/spidy/network)
[![Stars](https://img.shields.io/github/stars/rivermont/spidy.svg?style=social&label=Stars)](https://github.com/rivermont/spidy/stargazers)

Created by [rivermont](https://github.com/rivermont) (/rɪvɜːrmɒnt/) and [FalconWarriorr](https://github.com/FalconWarriorr) (/fælcʌnraɪjɔːr/), and developed with help from [these awesome people](https://github.com/rivermont/spidy#contributors).<br>
Looking for technical documentation? Check out [`DOCS.md`](https://github.com/rivermont/spidy/blob/master/spidy/docs/DOCS.md)<br>
Looking to contribute to this project? Have a look at [`CONTRIBUTING.md`](https://github.com/rivermont/spidy/blob/master/spidy/docs/CONTRIBUTING.md), then check out the docs.

***

# 🎉 New Features!

### Multithreading
Crawl all the things! Run separate threads to work on multiple pages at the same time.<br>
Such fast. Very wow.

### PyPI
Install spidy with one line: `pip install spidy-web-crawler`!

### Automatic Testing with Travis CI

### Release v1.4.0 - #[31663d3](https://github.com/rivermont/spidy/commit/31663d34ceeba66ea9de9819b6da555492ed6a80)
[spidy Web Crawler Release 1.4](https://github.com/rivermont/spidy/releases/tag/1.4.0)


# Contents

  - [spidy Web Crawler](https://github.com/rivermont/spidy#spidy-web-crawler)
  - [New Features!](https://github.com/rivermont/spidy#-new-features)
  - [Contents](https://github.com/rivermont/spidy#contents)
  - [How it Works](https://github.com/rivermont/spidy#how-it-works)
  - [Why It's Different](https://github.com/rivermont/spidy#why-its-different)
  - [Features](https://github.com/rivermont/spidy#features)
  - [Tutorial](https://github.com/rivermont/spidy#tutorial)
    - [Using with Docker](https://github.com/rivermont/spidy#using-with-docker)
    - [Installing from PyPI](https://github.com/rivermont/spidy#installing-from-pypi)
    - [Installing from Source Code](https://github.com/rivermont/spidy#installing-from-source-code)
      - [Python Installation](https://github.com/rivermont/spidy#python-installation)
        - [Windows and Mac](https://github.com/rivermont/spidy#windows-and-mac)
          - [Anaconda](https://github.com/rivermont/spidy#anaconda)
          - [Python Base](https://github.com/rivermont/spidy#python-base)
        - [Linux](https://github.com/rivermont/spidy#linux)
      - [Crawler Installation](https://github.com/rivermont/spidy#crawler-installation)
      - [Launching](https://github.com/rivermont/spidy#launching)
      - [Running](https://github.com/rivermont/spidy#running)
        - [Config](https://github.com/rivermont/spidy#config)
        - [Start](https://github.com/rivermont/spidy#start)
        - [Autosave](https://github.com/rivermont/spidy#autosave)
        - [Force Quit](https://github.com/rivermont/spidy#force-quit)
  - [How Can I Support This?](https://github.com/rivermont/spidy#how-can-i-support-this)
  - [Contributors](https://github.com/rivermont/spidy#contributors)
  - [License](https://github.com/rivermont/spidy#license)


# How it Works
Spidy has two working lists, `TODO` and `DONE`.<br>
'TODO' is the list of URLs it hasn't yet visited.<br>
'DONE' is the list of URLs it has already been to.<br>
The crawler visits each page in TODO, scrapes the DOM of the page for links, and adds those back into TODO.<br>
It can also save each page, because datahoarding 😜.


# Why It's Different
What sets spidy apart from other web crawling solutions written in Python?

Most of the other options out there are not web crawlers themselves, simply frameworks and libraries through which one can create and deploy a web spider for example Scrapy and BeautifulSoup.
Scrapy is a Web crawling framework, written in Python, specifically created for downloading, cleaning and saving data from the web whereas BeautifulSoup is a parsing library that allows a programmer to get specific elements out of a webpage but BeautifulSoup alone is not enough because you have to actually get the webpage in the first place.

But with Spidy, everything runs right out of the box.
Spidy is a Web Crawler which is easy to use and is run from the command line. You have to give it a URL link of the webpage and it starts crawling away! A very simple and effective way of fetching stuff off of the web. 



# Features
We built a lot of the functionality in spidy by watching the console scroll by and going, "Hey, we should add that!"<br>
Here are some features we figure are worth noting.

  - Error Handling: We have tried to recognize all of the errors spidy runs into and create custom error messages and logging for each. There is a set cap so that after accumulating too many errors the crawler will stop itself.
  - Cross-Platform compatibility: spidy will work on all three major operating systems, Windows, Mac OS/X, and Linux!
  - Frequent Timestamp Logging: Spidy logs almost every action it takes to both the console and one of two log files.
  - Browser Spoofing: Make requests using User Agents from 4 popular web browsers, use a custom spidy bot one, or create your own!
  - Portability: Move spidy's folder and its contents somewhere else and it will run right where it left off. *Note*: This only works if you run it from source code.
  - User-Friendly Logs: Both the console and log file messages are simple and easy to interpret, but packed with information.
  - Webpage saving: Spidy downloads each page that it runs into, regardless of file type. The crawler uses the HTTP `Content-Type` header returned with most files to determine the file type.
  - File Zipping: When autosaving, spidy can archive the contents of the `saved/` directory to a `.zip` file, and then clear `saved/`.


# Tutorial

## Using with Docker
Spidy can be easily run in a Docker container.<br>

- First, build the [`Dockerfile`](dockerfile): `docker build -t spidy .`
  - Verify that the Docker image has been created: `docker images`
- Then, run it: `docker run --rm -it -v $PWD:/data spidy`
  - `--rm` tells Docker to clean up after itself by removing stopped containers.
  - `-it` tells Docker to run the container interactively and allocate a pseudo-TTY.
  - `-v $PWD:/data` tells Docker to mount the current working directory as `/data` directory inside the container. This is needed if you want Spidy's files (e.g. `crawler_done.txt`, `crawler_words.txt`, `crawler_todo.txt`) written back to your host filesystem.

### Spidy Docker Demo

![Spidy Docker Demo](media/spidy_docker_demo.gif)

## Installing from PyPI
Spidy can be found on the Python Package Index as `spidy-web-crawler`.<br>
You can install it from your package manager of choice and simple run the `spidy` command.<br>
The working files will be found in your home directory.

## Installing from Source Code
Alternatively, you can download the source code and run it.

### Python Installation
The way that you will run spidy depends on the way you have Python installed.<br>

#### Windows and Mac

There are many different versions of [Python](https://www.python.org/about/), and hundreds of different installations for each them.<br>
Spidy is developed for Python v3.5.2, but should run without errors in other versions of Python 3.

##### Anaconda
We recommend the [Anaconda distribution](https://www.continuum.io/downloads).<br>
It comes pre-packaged with lots of goodies, including `lxml`, which is required for spidy to run and not including in the standard Python package.

##### Python Base
You can also just install [default Python](https://www.python.org/downloads/), and install the external libraries separately.<br>
This can be done with `pip`:

    pip install -r requirements.txt

#### Linux
Python 3 should come preinstalled with most flavors of Linux, but if not, simply run

    sudo apt update
    sudo apt install python3 python3-lxml python3-requests

Then `cd` into the crawler's directory and run `python3 crawler.py`.

### Crawler Installation
If you have git or GitHub Desktop installed, you can clone the repository [from here](https://github.com/rivermont/spidy.git). If not, download [the latest source code](https://github.com/rivermont/spidy/archive/master.zip) or grab the [latest release](https://github.com/rivermont/spidy/releases).

### Launching

Use `cd` to navigate to the directory that spidy is located in, then run:

    python crawler.py

![](https://raw.githubusercontent.com/rivermont/spidy/master/media/run.gif)

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

#### Start
Sample start log.

![](https://raw.githubusercontent.com/rivermont/spidy/master/media/start.png)

#### Autosave
Sample log after hitting the autosave cap.

![](https://raw.githubusercontent.com/rivermont/spidy/master/media/log.png)

#### Force Quit
Sample log after performing a `^C` (CONTROL + C) to force quit the crawler.

![](https://raw.githubusercontent.com/rivermont/spidy/master/media/keyboardinterrupt.png)


# How Can I Support This?
The easiest thing you can do is Star spidy if you think it's cool, or Watch it if you would like to get updates.<br>
If you have a suggestion, [create an Issue](https://github.com/rivermont/spidy/issues/new) or Fork the `master` branch and open a Pull Request.


# Contributors
See the [`CONTRIBUTING.md`](https://github.com/rivermont/spidy/blob/master/spidy/docs/CONTRIBUTING.md)

* The logo was designed by [Cutwell](https://github.com/Cutwell)

* [3onyc](https://github.com/3onyc) - PEP8 Compliance.
* [DeKaN](https://github.com/DeKaN) - Getting PyPI packaging to work.
* [esouthren](https://github.com/esouthren) - Unit testing.
* [Hrily](https://github.com/Hrily) - Multithreading.
* [j-setiawan](https://github.com/j-setiawan) - Paths that work on all OS's.
* [michellemorales](https://github.com/michellemorales) - Confirmed OS/X support.
* [petermbenjamin](https://github.com/petermbenjamin) - Docker support.
* [quatroka](https://github.com/quatroka) - Fixed testing bugs.
* [stevelle](https://github.com/stevelle) - Respect robots.txt.
* [thatguywiththatname](https://github.com/thatguywiththatname) - README link corrections.

# License
We used the [Gnu General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html) (see [`LICENSE`](https://github.com/rivermont/spidy/blob/master/LICENSE)) as it was the license that best suited our needs.<br>
Honestly, if you link to this repo and credit `rivermont` and `FalconWarriorr`, and you aren't selling spidy in any way, then we would love for you to distribute it.<br>
Thanks!

***
