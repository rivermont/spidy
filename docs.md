# spidy Web Crawler
Spidy (/spˈɪdi/) is the simple, easy to use command line web crawler.<br>
This is the very technical documentation file.<br>
Heads up: We have no idea how to do this! If you wish to help please do, just edit and make a Pull Request!<br>
If you're looking for the plain English, check out the [README](https://github.com/rivermont/spidy).

--------------------

# Table of Contents

  - [spidy](#spidy-web-crawler)
  - [Table of Contents](#table-of-contents)
  - [Errors](#errors)
    - [HeaderError](#headererror--source)
  - [Functions](#functions)
    - [mime_lookup](#mime_lookup--source]
  - [Global Variables](#global-variables)
    - [MIME_TYPES](#mime_types--source)
	- [VERSION](#version--source)


# Errors
This section lists the custom Erorrs and Exceptions in `crawler.py` that may be raised throughout the code.

## HeaderError - [Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L50))
Can be raised when there is a problem deciphering HTTP headers returned from a website.


# Functions
This section lists the functions in `crawler.py` that are used throughout the code.

## `mime_lookup` - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L171))
This finds the correct file extension for a MIME type using the [`MIME_TYPES`](#mime_types--source) dictionary.<br>
If the MIME type is blank it defaults to `.html`, and if the MIME type is not in the dictionary a [`HeaderError`](#headererror--source) is raised.<br>
Usage:

> mime_lookup(value)

Where `value` is the MIME type.


# Global Variables
This section lists the variables in [`crawler.py`](#https://github.om/rivermont/spidy/blob/master/crawler.py) that are used throughout the code.

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

## VERSION - ([Source](https://github.com/rivermont/spidy/blob/master/crawler.py#L5))
The current version of the crawler.
