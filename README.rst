spidy Web Crawler
=================

Spidy (/spˈɪdi/) is the simple, easy to use command line web crawler.
Given a list of web links, it uses Python
```requests`` <http://docs.python-requests.org>`__ to query the
webpages, and ```lxml`` <http://lxml.de/index.html>`__ to extract all
links from the page. Pretty simple!

|spidy Logo|

|Version: 1.5.1| |Release: 1.4.0| |License: GPL v3| |Python 3.3+| |All
Platforms!| |Open Source Love| |Lines of Code: 1437| |Lines of Docs:
564| |Last Commit| |Travis CI Status| |Contributors| |Forks| |Stars|

Created by `rivermont <https://github.com/rivermont>`__ (/rɪvɜːrmɒnt/)
and `FalconWarriorr <https://github.com/Casillas->`__ (/fælcʌnraɪjɔːr/),
and developed with help from `these awesome
people <https://github.com/rivermont/spidy#contributors>`__. Looking for
technical documentation? Check out
`DOCS.md <https://github.com/rivermont/spidy/blob/master/docs/DOCS.md>`__\ 
Looking to contribute to this project? Have a look at
```CONTRIBUTING.md`` <https://github.com/rivermont/spidy/blob/master/docs/CONTRIBUTING.md>`__,
then check out the docs.

--------------

🎉 New Features!
================

PyPI
~~~~

Install spidy with one line: ``pip3 install spidy-web-crawler``!

Automatic Testing with Travis CI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Release v1.4.0 - #\ `31663d3 <https://github.com/rivermont/spidy/commit/31663d34ceeba66ea9de9819b6da555492ed6a80>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`spidy Web Crawler Release
1.4 <https://github.com/rivermont/spidy/releases/tag/1.4.0>`__

Domain Limiting - #\ `e229b01 <https://github.com/rivermont/spidy/commit/e229b01eed7e1f95530d06afc671e40dbf4dac53>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Scrape only a single site instead of the whole internet. May use
slightly less space on your disk. See ``config/wsj.cfg`` for an example.

Contents
========

-  `spidy Web
   Crawler <https://github.com/rivermont/spidy#spidy-web-crawler>`__
-  `New Features! <https://github.com/rivermont/spidy#-new-features>`__
-  `Contents <https://github.com/rivermont/spidy#contents>`__
-  `How it Works <https://github.com/rivermont/spidy#how-it-works>`__
-  `Features <https://github.com/rivermont/spidy#features>`__
-  `Tutorial <https://github.com/rivermont/spidy#tutorial>`__

   -  `Python
      Installation <https://github.com/rivermont/spidy#python-installation>`__
   -  `Windows and
      Mac <https://github.com/rivermont/spidy#windows-and-mac>`__

      -  `Anaconda <https://github.com/rivermont/spidy#anaconda>`__
      -  `Python
         Base <https://github.com/rivermont/spidy#python-base>`__

   -  `Linux <https://github.com/rivermont/spidy#linux>`__
   -  `Crawler
      Installation <https://github.com/rivermont/spidy#crawler-installation>`__
   -  `Launching <https://github.com/rivermont/spidy#launching>`__
   -  `Running <https://github.com/rivermont/spidy#running>`__
   -  `Config <https://github.com/rivermont/spidy#config>`__
   -  `Start <https://github.com/rivermont/spidy#start>`__
   -  `Autosave <https://github.com/rivermont/spidy#autosave>`__
   -  `Force Quit <https://github.com/rivermont/spidy#force-quit>`__

-  `Contributors <https://github.com/rivermont/spidy#contributors>`__
-  `License <https://github.com/rivermont/spidy#license>`__

How it Works
============

Spidy has two working lists, ``TODO`` and ``DONE``. TODO is the list of
URLs it hasn't yet visited. Done is the list of URLs it has already been
to. The crawler visits each page in TODO, scrapes the DOM of the page
for links, and adds those back into TODO. It can also save each page,
because datahoarding 😜.

Features
========

We built a lot of the functionality in spidy by watching the console
scroll by and going, "Hey, we should add that!" Here are some features
we figure are worth noting.

-  Error Handling: We have tried to recognize all of the errors spidy
   runs into and create custom error messages and logging for each.
   There is a set cap so that after accumulating too many errors the
   crawler will stop itself.
-  Cross-Platform compatability: spidy will work on all three major
   operatin systems, Windows, Mac OS/X, and Linux!
-  Frequent Timestamp Logging: Spidy logs almost every action it takes
   to both the console and one of two log files.
-  Browser Spoofing: Make requests using User Agents from 4 popular web
   browsers, use a custom spidy bot one, or create your own!
-  Portability: Move spidy's folder and its contents somewhere else and
   it will run right where it left off. *Note*: This only works if you
   run it from source code.
-  User-Friendly Logs: Both the console and log file messages are simple
   and easy to interpret, but packed with information.
-  Webpage saving: Spidy downloads each page that it runs into,
   regardless of file type. The crawler uses the HTTP ``Content-Type``
   header returned with most files to determine the file type.
-  File Zipping: When autosaving, spidy can archive the contents of the
   ``saved/`` directory to a ``.zip`` file, and then clear ``saved/``.

Tutorial
========

The way that you will run spidy depends on the way you have Python
installed.

Installing from PyPI
--------------------

Spidy can be found on the Python Package Index as ``spidy-web-crawler``.
You can install it from your package manager of choice and simple run
the ``spidy`` command. The working files will be found in your home
directory.

Installing from Source Code
---------------------------

Alternatively, you can download the source code and run it.

Python Installation
~~~~~~~~~~~~~~~~~~~

Windows and Mac
^^^^^^^^^^^^^^^

There are many different versions of
`Python <https://www.python.org/about/>`__, and hundreds of different
installations for each them. Spidy is developed for Python v3.5.2, but
should run without errors in other versions of Python 3.

Anaconda
''''''''

We recommend the `Anaconda
distribution <https://www.continuum.io/downloads>`__. It comes
pre-packaged with lots of goodies, including ``lxml``, which is required
for spidy to run and not including in the standard Python package.

Python Base
'''''''''''

You can also just install `default
Python <https://www.python.org/downloads/>`__, and install the external
libraries separately. This can be done with ``pip``:

::

    pip install -r requirements.txt

Linux
^^^^^

Python 3 should come preinstalled with most flavors of Linux, but if
not, simply run

::

    sudo apt update
    sudo apt install python3 python3-lxml python3-requests

Then ``cd`` into the crawler's directory and run ``python3 crawler.py``.

Crawler Installation
~~~~~~~~~~~~~~~~~~~~

If you have git or GitHub Desktop installed, you can clone the
repository `from here <https://github.com/rivermont/spidy.git>`__. If
not, download `the latest source
code <https://github.com/rivermont/spidy/archive/master.zip>`__ or grab
the `latest release <https://github.com/rivermont/spidy/releases>`__.

Launching
^^^^^^^^^

Use ``cd`` to navigate to the directory that spidy is located in, then
run:

::

    python crawler.py

.. figure:: /media/run.gif?raw=true
   :alt: 

Running
^^^^^^^

Spidy logs a lot of information to the command line throughout its life.
Once started, a bunch of ``[INIT]`` lines will print. These announce
where spidy is in its initialization process.

Config
''''''

On running, spidy asks for input regarding certain parameters it will
run off of. However, you can also use one of the configuration files, or
even create your own.

To use spidy with a configuration file, input the name of the file when
the crawler asks

The config files included with spidy are:

-  *``blank.txt``*: Template for creating your own configurations.
-  ``default.cfg``: The default version.
-  ``heavy.cfg``: Run spidy with all of its features enabled.
-  ``infinite.cfg``: The default config, but it never stops itself.
-  ``light.cfg``: Disable most features; only crawls pages for links.
-  ``rivermont.cfg``: My personal favorite settings.
-  ``rivermont-infinite.cfg``: My favorite, never-ending configuration.

Start
^^^^^

Sample start log.

.. figure:: /media/start.png?raw=true
   :alt: 

Autosave
^^^^^^^^

Sample log after hitting the autosave cap.

.. figure:: /media/log.png?raw=true
   :alt: 

Force Quit
^^^^^^^^^^

Sample log after performing a ``^C`` (CONTROL + C) to force quit the
crawler.

.. figure:: /media/keyboardinterrupt.png?raw=true
   :alt: 

Contributors
============

-  The logo was designed by `Cutwell <https://github.com/Cutwell>`__

-  `3onyc <https://github.com/3onyc>`__ - PEP8 Compliance.
-  `DeKaN <https://github.com/DeKaN>`__ - Getting PyPI packaging to
   work.
-  `esouthren <https://github.com/esouthren>`__ - Unit testing.
-  `j-setiawan <https://github.com/j-setiawan>`__ - Paths that work on
   all OS's.
-  `michellemorales <https://github.com/michellemorales>`__ - Confirmed
   OS/X support.
-  `quatroka <https://github.com/quatroka>`__ - Fixed testing bugs.
-  `stevelle <https://github.com/stevelle>`__ - Respect robots.txt.
-  `thatguywiththatname <https://github.com/thatguywiththatname>`__ -
   README link corrections

License
=======

We used the `Gnu General Public
License <https://www.gnu.org/licenses/gpl-3.0.en.html>`__ (see
`LICENSE <https://github.com/rivermont/spidy/blob/master/LICENSE>`__) as
it was the license that best suited our needs. Honestly, if you link to
this repo and credit ``rivermont`` and ``FalconWarriorr``, and you
aren't selling spidy in any way, then we would love for you to
distribute it. Thanks!

--------------

.. |spidy Logo| image:: https://raw.githubusercontent.com/rivermont/spidy/master/media/spidy_logo.png
   :target: https://github.com/rivermont/spidy#contributors
.. |Version: 1.5.1| image:: https://img.shields.io/badge/version-1.5.1-brightgreen.svg
.. |Release: 1.4.0| image:: https://img.shields.io/github/release/rivermont/spidy.svg
   :target: https://github.com/rivermont/spidy/releases
.. |License: GPL v3| image:: https://img.shields.io/badge/license-GPLv3.0-blue.svg
   :target: http://www.gnu.org/licenses/gpl-3.0
.. |Python 3.3+| image:: https://img.shields.io/badge/python-3.3+-brightgreen.svg
   :target: https://docs.python.org/3/
.. |All Platforms!| image:: https://img.shields.io/badge/Windows,%20OS/X,%20Linux-%20%20-brightgreen.svg
.. |Open Source Love| image:: https://badges.frapsoft.com/os/v1/open-source.png?v=103
.. |Lines of Code: 1437| image:: https://img.shields.io/badge/lines%20of%20code-1437-brightgreen.svg
.. |Lines of Docs: 564| image:: https://img.shields.io/badge/lines%20of%20docs-564-orange.svg
.. |Last Commit| image:: https://img.shields.io/github/last-commit/rivermont/spidy.svg
   :target: https://github.com/rivermont/spidy/graphs/punch-card
.. |Travis CI Status| image:: https://img.shields.io/travis/rivermont/spidy/master.svg
   :target: https://travis-ci.org/rivermont/spidy
.. |Contributors| image:: https://img.shields.io/github/contributors/rivermont/spidy.svg
   :target: https://github.com/rivermont/spidy/graphs/contributors
.. |Forks| image:: https://img.shields.io/github/forks/rivermont/spidy.svg?style=social&label=Forks
   :target: https://github.com/rivermont/spidy/network
.. |Stars| image:: https://img.shields.io/github/stars/rivermont/spidy.svg?style=social&label=Stars
   :target: https://github.com/rivermont/spidy/stargazers
