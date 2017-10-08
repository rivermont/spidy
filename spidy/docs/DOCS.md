# spidy Web Crawler
Spidy (/spˈɪdi/) is the simple, easy to use command line web crawler.<br>
This is the very technical documentation file.<br>
Heads up: We have no idea how to do this! If you wish to help please do, just edit and make a Pull Request!<br>

If you're looking for the plain English, check out the [README](https://github.com/rivermont/spidy).<br>
See [`CONTRIBUTING.md`](https://github.com/rivermomnt/spidy/blob/master/docs/CONTRIBUTING.md) for some guidelines on how to get started.

Bad Stuff: [![Open Issues](https://img.shields.io/github/issues/rivermont/spidy.svg)](https://github.com/rivermont/spidy/issues)
[![Open Pull Requests](https://img.shields.io/github/issues-pr/rivermont/spidy.svg)](https://github.com/rivermont/spidy/pulls)
<br>
Good Stuff: [![Closed Issues](https://img.shields.io/github/issues-closed/rivermont/spidy.svg)](https://github.com/rivermont/spidy/issues?q=is%3Aissue+is%3Aclosed)
[![Closed Pull Requests](https://img.shields.io/github/issues-pr-closed/rivermont/spidy.svg)](https://github.com/rivermont/spidy/pulls?q=is%3Apr+is%3Aclosed)

***

# Table of Contents

  - [spidy](https://github.com/rivermont/spidy/blob/master/docs/DOCS.md#spidy-web-crawler)
  - [Table of Contents](https://github.com/rivermont/spidy/blob/master/docs/DOCS.md#table-of-contents)
  - [Info](https://github.com/rivermont/spidy/blob/master/docs/DOCS.md#info)
  - [GUI](https://github.com/rivermont/spidy/blob/master/docs/DOCS.md#gui)
  - [Files](https://github.com/rivermont/spidy/blob/master/docs/DOCS.md#files)
    - [Save Files](https://github.com/rivermont/spidy/blob/master/docs/DOCS.md#save-files)
    - [Run Files](https://github.com/rivermont/spidy/blob/master/docs/DOCS.md#run-files)
  - [Branches](https://github.com/rivermont/spidy/blob/master/docs/DOCS.md#branches)
  - [Classes](https://github.com/rivermont/spidy/blob/master/docs/DOCS.md#Classes)
  - [Functions](https://github.com/rivermont/spidy/blob/master/docs/DOCS.md#functions)
  - [Global Variables](https://github.com/rivermont/spidy/blob/master/docs/DOCS.md#global-variables)


# Info
General information and thoughts about spidy.

A good read about web crawlers and some theory that goes with them is Michael Nielson's [How to crawl a quarter billion webpages in 40 hours](http://www.michaelnielsen.org/ddi/how-to-crawl-a-quarter-billion-webpages-in-40-hours/).<br>
It helped me understand how a web crawler should run, and is just a good article in general.


# GUI

The original plan for a spidy GUI was an interface for those who prefer clicky things other command line.<br>
Users would select options from dropdowns, checkboxes, and text fields instead of using a config file or entering them in the console. A textbox would hold the console output, and there would be counters for errors, pages crawled, etc.<br>
Eventually having the crawler and GUI bundled into an exe - created with something like [py2exe](http://py2exe.org/) - would be great.

[Here](https://raw.githubusercontent.com/rivermont/spidy/master/media/frame.png) is a rough wireframe of the original idea.


# Files

### config/
Contains configuration files.

### media/
Contains images used in this README file.

## Save Files
Some of these files will be created when `crawler.py` is first run.

### crawler_todo.txt
Contains all of the links that spidy has found but not yet crawled.

### crawler_done.txt
Contains all of the links that spidy has already visited.

### crawler_bad.txt
Contains all of the links that caused errors for some reason.

### crawler_words.txt
Contains all of the words that spidy has found.

## Run Files

### crawler.py
The important code. This is what you will run to crawl links and save information.<br>
Because the internet is so big, this will practically never end.

### gui.py
The development file for the GUI.

### spidy.bat
Windows Batch file for running the crawler.


# Branches

## master
The stable, up-to-date branch.

## FalconWarriorr-branch
Falconwarriorr's branch.<br>
He has developed a bunch of features that we are working on merging into master.


***

Everything that follows is intended to be detailed information on each piece in `crawler.py`. There's a lot of 'TODO's, though!

# Classes
This section lists the custom classes in `crawler.py`.<br>
Most are Errors or Exceptions that may be raised throughout the code.

## `HeaderError` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L65))
Raised when there is a problem deciphering HTTP headers returned from a website.

## `SizeError` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L72))
Raised when a file is too large to download in an acceptable time.


# Functions
This section lists the functions in `crawler.py` that are used throughout the code.

## `check_link` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L122))
Determines whether links should be crawled.<br>
Types of links that will be pruned:

  - Links that are too long or short.
  - Links that don't start with `http(s)`.
  - Links that have already been crawled.
  - Links in [`KILL_LIST`](https://github.com/rivermont/spidy/blob/master/docs/DOCS.md#kill_list--source).

## `check_path` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L154))
Checks whether a file path will cause errors when saving.<br>
Paths longer than 256 characters cannot be saved (Windows).

## `check_word` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L142))
Checks whether a word is valid.<br>
The word-saving feature was originally added to be used for password cracking with hashcat, which is why `check_word` checks for length of less than 16 characters.<br>
The average password length is around 8 characters.

## `crawl` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L86))
Does all of the crawling, scraping, scraping of a single document.

## `err_log` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L323))
Saves the triggering error to the log file.

## `get_mime_type` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L218))
Extracts the Content-Type header from the headers returned by page.

## `get_time` - ([Source](https://github.com/rivermont/spidy/blobl/master/crawler.py#L18))
Returns the current time in the format `HH:MM::SS`.

## `get_full_time` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L22))
Returns the current time in the format `HH:MM:SS, Day, Mon, YYYY`.

## `handle_keyboard_interrupt` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L307))
Shuts down the crawler when a `KeyboardInterrupt` is performed.

## `info_log` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L278))
Logs important information to the console and log file.<br>
Example log:

    [23:17:06] [spidy] [INFO]: Queried 100 links.
    [23:17:06] [spidy] [INFO]: Started at 23:15:33.
    [23:17:06] [spidy] [INFO]: Log location: logs/spidy_log_1499483733
    [23:17:06] [spidy] [INFO]: Error log location: logs/spidy_error_log_1499483733.txt
    [23:17:06] [spidy] [INFO]: 1901 links in TODO.
    [23:17:06] [spidy] [INFO]: 110446 links in done.
    [23:17:06] [spidy] [INFO]: 0/5 new errors caught.
    [23:17:06] [spidy] [INFO]: 0/20 HTTP errors encountered.
    [23:17:06] [spidy] [INFO]: 1/10 new MIMEs found.
    [23:17:06] [spidy] [INFO]: 3/20 known errors caught.
    [23:17:06] [spidy] [INFO]: Saving files...
    [23:17:06] [spidy] [LOG]: Saved TODO list to crawler_todo.txt
    [23:17:06] [spidy] [LOG]: Saved done list to crawler_done.txt
    [23:17:06] [spidy] [LOG]: Saved 90 bad links to crawler_bad.txt

## `log` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L295))
Logs a single message to the error log file.
Prints message verbatim, so message must be formatted correctly in the function call.

## `make_file_path` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L205))
Makes a valid Windows file path for a given url.

## `make_words` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L166))
Returns a list of all the valid words (determined using [`check_word`](https://github.com/rivermont/spidy/blob/master/docs/DOCS.md#check_word--source)) on a given page.

## `mime_lookup` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L229))
This finds the correct file extension for a MIME type using the [`MIME_TYPES`](https://github.com/rivermont/spidy/blob/master/docs/DOCS.md#mime_types--source) dictionary.<br>
If the MIME type is blank it defaults to `.html`, and if the MIME type is not in the dictionary a [`HeaderError`](https://github.com/rivermont/spidy/blob/master/docs/DOCS.md#headererror--source) is raised.<br>
Usage:

    mime_lookup(value)

Where `value` is the MIME type.

## `save_files` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L180))
Saves the TODO, DONE, word, and bad lists to their respective files.<br>
The word and bad link lists use the same function to save space.

## `save_page` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L245))
Download content of url and save to the `save` folder.

## `update_file` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L263))
TODO

## `write_log` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L42)
Writes message to both the console and the log file.<br>
NOTE: Automatically adds timestamp and `[spidy]` to message, and formats message for log appropriately.

## `zip_saved_files` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L336))
TODO


# Global Variables
This section lists the variables in [`crawler.py`](https://github.om/rivermont/spidy/blob/master/crawler.py) that are used throughout the code.

## `COUNTER` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L507))
Incremented each time a link is crawled.<br>
TODO

## `CRAWLER_DIR` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L30))
The directory that `crawler.py` is located in.

## `DOMAIN` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L523))
TODO

## `DONE` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L529))
TODO

## `DONE_FILE` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L528))
TODO

## `ERR_LOG_FILE` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L453))
TODO

## `ERR_LOG_FILE_NAME` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L454))
TODO

## `HEADER` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L522))
TODO

## `HEADERS` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L457))
TODO

## `HTTP_ERROR_COUNT` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L514))
TODO

## `KILL_LIST` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L495))
A list of pages that are known to cause problems with the crawler.

  - `bhphotovideo.com/c/search`
  - `scores.usaultimate.org/`: Never responds.
  - `w3.org`: I have never been able to access W3, although it never says it's down. If someone knows of this problem, please let me know.
  - `web.archive.org/web/`: While there is some good content, there are sometimes thousands of copies of the same exact page. Not good for web crawling.

## `KNOWN_ERROR_COUNT` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L509))
TODO

## `LOG_END` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L504))
Line to print at the end of each `logFile` log

## `LOG_FILE` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L38))
The file that the command line logs are written to.<br>
Kept open until the crawler stops for whatever reason so that it can be written to.

## `LOG_FILE_NAME`  - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L39))
The actual file name of [`LOG_FILE`](#log_file--source).<br>
Used in [`info_log`](#info_log--source).

## `MAX_HTTP_ERRORS` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L523))
TODO

## `MAX_KNOWN_ERRORS` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L523))
TODO

## `MAX_NEW_ERRORS` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L523))
TODO

## `MAX_NEW_MIMES` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L524))
TODO

## `MIME_TYPES` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L354))
A dictionary of [MIME types](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types) encountered by the crawler.<br>
While there are [thousands of other types](https://www.iana.org/assignments/media-types/media-types.xhtml) that are not listed, to list them all would be impractical:
  - The size of the list would be huge, using memory, space, etc.
  - Lookup times would likely be much longer due to the size.
  - Many of the types are outdated or rarely used.
However there are many incorrect usages out there, as the list shows.
  - `text/xml`, `text/rss+xml` are both wrong for RSS feeds: [StackOverflow](https://stackoverflow.com/q/595616/4381663)
  - `html` should never be used. Only `text/html`.

The extension for a MIME type can be found using the dictionary itself or by calling `mime_lookup(value)`<br>
To use the dictionary, use:

    MIME_TYPES[value]

Where `value` is the MIME type.<br>
This will return the extension associated with the MIME type if it exists, however this will throw an [`IndexError`](https://docs.python.org/2/library/exceptions.html#exceptions.IndexError) if the MIME type is not in the dictionary.<br>
Because of this, it is recommended to use the [`mime_lookup`](#mime_lookup--source) function.

## `NEW_ERROR_COUNT` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L508))
TODO

## `NEW_MIME_COUNT` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L511))
TODO

## `OVERRIDE_SIZE` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L526))
TODO

## `OVERWRITE` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L526))
TODO

## `RAISE_ERRORS` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L526))
TODO

## `RESTRICT` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L525))
TODO

## `SAVE_COUNT` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L523))
TODO

## `SAVE_PAGES` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L527))
TODO

## `SAVE_WORDS` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L527))
TODO

## `START` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L501))
Links to start crawling if the TODO list is empty

## `START_TIME` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L20))
The time that `crawler.py` was started, in seconds from the epoch.<br>
More information can be found on the page for the Python [time](https://docs.python.org/3/library/time.html) library.

## `START_TIME_LONG` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L21))
The time that `crawler.py` was started, in the format `HH:MM:SS, Date Month Year`.<br>
Used in `info_log`.

## `TODO` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L529))
The list containing all links that are yet to be crawled.

## `TODO_FILE` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L528))
TODO

## `USE_CONFIG` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L523))
TODO

## `VERSION` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L13))
The current version of the crawler.

## `WORD_FILE` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L528))
TODO

## `WORDS` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L514))
TODO

## `ZIP_FILES` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L526))
TODO

***
