# spidy Web Crawler
Spidy (/spˈɪdi/) is the simple, easy to use command line web crawler.<br>
This is the very technical documentation file.<br>
Heads up: We have no idea how to do this! If you wish to help please do, just edit and make a Pull Request!<br>
If you're looking for the plain English, check out the [README](https://github.com/rivermont/spidy).

--------------------

# Table of Contents

  - [spidy](#spidy-web-crawler)
  - [Table of Contents](#table-of-contents)
  - [Info](#info)
  - [Errors](#errors)
    - [HeaderError](#headererror--source)
  - [Functions](#functions)
    - [check_link](#check_link--source)
	- [check_path](#check_path--source)
	- [check_word](#check_word--source)
	- [info_log](#info_log--source)
	- [make_words](#make_words--source)
    - [mime_lookup](#mime_lookup--source)
	- [save_files](#save_files--source)
  - [Global Variables](#global-variables)
    - [CRAWLER_DIR](#crawler_dir--source)
	- [KILL_LIST](#kill_list--source)
	- [LOG_FILE](#log_file--source)
	- [LOG_FILE_NAME](#log_file_name--source)
    - [MIME_TYPES](#mime_types--source)
	- [START_TIME](#start_time--source)
	- [START_TIME_LONG](#start_time_long--source)
	- [VERSION](#version--source)


# Info
General information and thoughts about spidy.

A good read about web crawlers and some theory that goes with them is Michael Nielson's [How to crawl a quarter billion webpages in 40 hours](http://www.michaelnielsen.org/ddi/how-to-crawl-a-quarter-billion-webpages-in-40-hours/).<br>
It helped me understand how a web crawler should run, and is just a good article in general.


# Errors
This section lists the custom Errors and Exceptions in `crawler.py` that may be raised throughout the code.

## `HeaderError` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L50))
Raised when there is a problem deciphering HTTP headers returned from a website.


# Functions
This section lists the functions in `crawler.py` that are used throughout the code.

## `check_link` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L64))
Determines whether links should be crawled.<br>
Types of links that will be pruned:

  - Links that are too long or short.
  - Links that don't start with `http(s)`.
  - Links that have already been crawled.
  - Links in [`KILL_LIST`](#kill_list--source).

## `check_path` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L95))
Checks whether a file path will cause errors when saving.<br>
Paths longer than 256 characters cannot be saved (Windows).

## `check_word` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L84))
Checks whether a word is valid.<br>
The word-saving feature was originally added to be used for password cracking with hashcat, which is why `check_word` checks for length of less than 16 characters.<br>
The average password length is around 8 characters.

## `err_log` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L269))
TODO

## `err_print` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L255))
TODO

## `err_saved_message` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L262))
TODO

## `get_mime_type` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L159))
TODO

## `handle_KeyboardInterrupt` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L247))
TODO

## `info_log` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L209))
Logs important information to the console and log file.<br>
Example log:

> [23:17:06] [spidy] [INFO]: Queried 100 links.
> [23:17:06] [spidy] [INFO]: Started at 23:15:33.
> [23:17:06] [spidy] [INFO]: Log location: logs/spidy_log_1499483733
> [23:17:06] [spidy] [INFO]: Error log location: logs/spidy_error_log_1499483733.txt
> [23:17:06] [spidy] [INFO]: 1901 links in TODO.
> [23:17:06] [spidy] [INFO]: 110446 links in done.
> [23:17:06] [spidy] [INFO]: 0/5 new errors caught.
> [23:17:06] [spidy] [INFO]: 0/20 HTTP errors encountered.
> [23:17:06] [spidy] [INFO]: 1/10 new MIMEs found.
> [23:17:06] [spidy] [INFO]: 3/20 known errors caught.
> [23:17:06] [spidy] [INFO]: Saving files...
> [23:17:06] [spidy] [LOG]: Saved TODO list to crawler_todo.txt
> [23:17:06] [spidy] [LOG]: Saved done list to crawler_done.txt
> [23:17:06] [spidy] [LOG]: Saved 90 bad links to crawler_bad.txt

## `log` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L236))
TODO

## `make_file_path` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L147))
TODO

## `make_words` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L106))
Returns a list of all the valid words (determined using [`check_word`](#check_word--source)) on a given page.

## `mime_lookup` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L171))
This finds the correct file extension for a MIME type using the [`MIME_TYPES`](#mime_types--source) dictionary.<br>
If the MIME type is blank it defaults to `.html`, and if the MIME type is not in the dictionary a [`HeaderError`](#headererror--source) is raised.<br>
Usage:

> mime_lookup(value)

Where `value` is the MIME type.

## `save_files` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L119))
Saves the TODO, DONE, word, and bad lists to their respective files.<br>
The word and bad link lists use the same function to save space.

## `save_page` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L184))
TODO

## `update_file` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L197))
TODO

## `zip` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L281))
TODO


# Global Variables
This section lists the variables in [`crawler.py`](#https://github.om/rivermont/spidy/blob/master/crawler.py) that are used throughout the code.

## `BAD_LINKS` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L412))
TODO

## `COUNTER` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L418))
Incremented each time a link is crawled.<br>
TODO

## `CRAWLER_DIR` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L24))
The directory that `crawler.py` is located in.

## `ERR_LOG_FILE` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L367))
TODO

## `ERR_LOG_FILE_NAME` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L368))
TODO

## `GET_ARGS` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L432))
TODO

## `HEADERS` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L371))
TODO

## `HTTP_ERROR_COUNT` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L421))
TODO

## `KILL_LIST` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L403))
A list of pages that are known to cause problems with the crawler.

  - `scores.usaultimate.org/`: Never responds.
  - `w3.org`: I have never been able to access W3, although it never says it's down. If someone knows of this problem, please let me know.
  - `web.archive.org/web/`: While there is some good content, there are sometimes thousands of copies of the same exact page. Not good for web crawling.

## `KNOWN_ERROR_COUNT` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L420))
TODO

## `LOG_END` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L415))
TODO

## `LOG_FILE` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L27))
The file that the command line logs are written to.<br>
Kept open until the crawler stops for whatever reason so that it can be written to.

## `LOG_FILE_NAME`  - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L28))
The actual file name of [`LOG_FILE`](#log_file--source).<br>
Used in [`info_log`](#info_log--source).

## `MIME_TYPES` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L298))
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

> MIME_TYPES[value]

Where `value` is the MIME type.<br>
This will return the extension associated with the MIME type if it exists, however this will throw an [`IndexError`](https://docs.python.org/2/library/exceptions.html#exceptions.IndexError) if the MIME type is not in the dictionary.<br>
Because of this, it is recommended to use the [`mime_lookup`](#mime_lookup--source) function.

## `NEW_ERROR_COUNT` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L419))
TODO

## `NEW_MIME_COUNT` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L422))
TODO

## `START_TIME` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L15))
The time that `crawler.py` was started, in seconds from the epoch.<br>
More information can be found on the page for the Python [time](https://docs.python.org/3/library/time.html) library.

## `START_TIME_LONG` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L18))
The time that `crawler.py` was started, in the format `HH:MM:SS, Date Month Year`.<br>
Used in `info_log`.

## `VERSION` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L5))
The current version of the crawler.

## `WORDS` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L425))
TODO
