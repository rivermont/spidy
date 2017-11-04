#!/usr/bin/env python3
"""
spidy Web Crawler
Built by rivermont and FalconWarriorr
"""
import time
import shutil
import requests
import urllib
import threading
import queue
import logging

from os import path, makedirs
from copy import copy
from lxml import etree
from lxml.html import iterlinks, resolve_base_href
from reppy.robots import Robots

try:
    from spidy import __version__
except ImportError:
    from __init__ import __version__


VERSION = __version__


# Time statements.
# This is done before anything else to enable timestamp logging at every step
def get_time():
    return time.strftime('%H:%M:%S')


def get_full_time():
    return time.strftime('%H:%M:%S, %A %b %Y')


START_TIME = int(time.time())
START_TIME_LONG = get_time()

# Get current working directory of spidy
WORKING_DIR = path.realpath('.')
PACKAGE_DIR = path.dirname(path.realpath(__file__))

# Open log file for logging
try:
    makedirs(WORKING_DIR + '/logs')  # Attempts to make the logs directory
    makedirs(WORKING_DIR + '/saved')  # Attempts to make the saved directory
except OSError:
    pass  # Assumes only OSError wil complain if /logs already exists

LOG_FILE = open(path.join(WORKING_DIR, 'logs', 'spidy_log_{0}.txt'.format(START_TIME)),
                'w+', encoding='utf-8', errors='ignore')
LOG_FILE_NAME = path.join('logs', 'spidy_log_{0}'.format(START_TIME))

# Error log location
ERR_LOG_FILE = path.join(WORKING_DIR, 'logs', 'spidy_error_log_{0}.txt'.format(START_TIME))
ERR_LOG_FILE_NAME = path.join('logs', 'spidy_error_log_{0}.txt'.format(START_TIME))

LOGGER = logging.getLogger('SPIDY')
LOGGER.setLevel(logging.DEBUG)

# create file handler
handler = logging.FileHandler(ERR_LOG_FILE)
# minimum level logged: DEBUG (0)
handler.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to handler
handler.setFormatter(formatter)

# add ch to logger
LOGGER.addHandler(handler)

log_mutex = threading.Lock()


def write_log(operation, message, package='spidy', status='INFO', worker=0):
    """
    Writes message to both the console and the log file.

    Operations:
      INIT
      CRAWL
      SAVE
      LOG
      ERROR

    STATUSES:
      INFO
      ERROR
      INPUT

    PACKAGES:
      spidy
      reppy

    Worker 0 = Core
    """
    global LOG_FILE, log_mutex
    with log_mutex:
        now = get_time()
        message = '[{0}] [{1}] [WORKER #{2}] [{3}] [{4}]: {5}'\
                  .format(now, package, str(worker), operation, status, message)
        print(message)
        if not LOG_FILE.closed:
            LOG_FILE.write('\n' + message)


write_log('INIT', 'Starting spidy Web Crawler version {0}'.format(VERSION))
write_log('INIT', 'Report any problems to GitHub at https://github.com/rivermont/spidy')


###########
# CLASSES #
###########

write_log('INIT', 'Creating classes...')


class HeaderError(Exception):
    """
    Raised when there's a problem deciphering returned HTTP headers.
    """
    pass


class SizeError(Exception):
    """
    Raised when a file is too large to download in an acceptable time.
    """
    pass


class Counter(object):
    """
    Thread safe Counter
    """

    def __init__(self, value=0):
        # RawValue because we don't need it to create a Lock:
        self.val = value
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.val += 1

    def decrement(self):
        with self.lock:
            self.val -= 1

    def value(self):
        with self.lock:
            return self.val


class ThreadSafeSet(list):
    """
    Thread Safe set
    """

    def __init__(self):
        self.lock = threading.Lock()
        self._set = set()

    def get(self):
        with self.lock:
            return self._set.pop()

    def put(self, o):
        with self.lock:
            self._set.add(o)

    def get_all(self):
        with self.lock:
            return self._set

    def clear(self):
        with self.lock:
            self._set.clear()


class RobotsIndex(object):
    """
    Thread Safe Robots Index
    """
    def __init__(self, respect_robots, user_agent):
        self.respect_robots = respect_robots
        self.user_agent = user_agent
        self.lock = threading.Lock()
        self.index = {}

    def is_allowed(self, start_url):
        if self.respect_robots:
            return self._lookup(start_url)
        else:
            return True

    def size(self):
        return len(self.index)

    def _lookup(self, url):
        hostname = urllib.parse.urlparse(url).hostname
        if hostname not in self.index.keys():
            with self.lock:
                # check again to be sure
                if hostname not in self.index.keys():
                    self._remember(url)

        return self.index[hostname].allowed(url)

    def _remember(self, url):
        urlparsed = urllib.parse.urlparse(url)
        robots_url = url.replace(urlparsed.path, '/robots.txt')
        write_log('ROBOTS',
                  'Reading robots.txt file at: {0}'.format(robots_url),
                  package='reppy')
        robots = Robots.fetch(robots_url)
        checker = robots.agent(self.user_agent)
        self.index[urlparsed.hostname] = checker


#############
# FUNCTIONS #
#############

write_log('INIT', 'Creating functions...')


def crawl(url, thread_id=0):
    global WORDS, OVERRIDE_SIZE, HEADER, SAVE_PAGES, SAVE_WORDS
    if not OVERRIDE_SIZE:
        try:
            # Attempt to get the size in bytes of the document
            length = int(requests.head(url, headers=HEADER).headers['Content-Length'])
        except KeyError:  # Sometimes no Content-Length header is returned...
            length = 1
        if length > 524288000:  # If the page is larger than 500 MB
            raise SizeError
    # If the SizeError is raised it will be caught in the except block in the run section,
    # and the following code will not be run.
    page = requests.get(url, headers=HEADER)  # Get page
    word_list = []
    if SAVE_WORDS:
        word_list = make_words(page)
        for word in word_list:
            WORDS.put(word)
    try:
        # Pull out all links after resolving them using any <base> tags found in the document.
        links = [link for element, attribute, link, pos in iterlinks(resolve_base_href(page.content))]
    except etree.ParseError:
        # If the document is not HTML content this will return an empty list.
        links = []
    links = list(set(links))
    if SAVE_PAGES:
        save_page(url, page)
    if SAVE_WORDS:
        # Announce which link was crawled
        write_log('CRAWL', 'Found {0} links and {1} words on {2}'.format(len(links), len(word_list), url),
                  worker=thread_id)
    else:
        # Announce which link was crawled
        write_log('CRAWL', 'Found {0} links on {1}'.format(len(links), url),
                  worker=thread_id)
    return links


def crawl_worker(thread_id, robots_index):
    """
    Crawler worker thread method
    """

    # Declare global variables
    global VERSION, START_TIME, START_TIME_LONG
    global LOG_FILE, LOG_FILE_NAME, ERR_LOG_FILE_NAME
    global HEADER, WORKING_DIR, KILL_LIST
    global COUNTER, NEW_ERROR_COUNT, KNOWN_ERROR_COUNT, HTTP_ERROR_COUNT, NEW_MIME_COUNT
    global MAX_NEW_ERRORS, MAX_KNOWN_ERRORS, MAX_HTTP_ERRORS, MAX_NEW_MIMES
    global USE_CONFIG, OVERWRITE, RAISE_ERRORS, ZIP_FILES, OVERRIDE_SIZE, SAVE_WORDS, SAVE_PAGES, SAVE_COUNT
    global TODO_FILE, DONE_FILE, ERR_LOG_FILE, WORD_FILE
    global RESPECT_ROBOTS, RESTRICT, DOMAIN
    global WORDS, TODO, DONE, THREAD_RUNNING

    while THREAD_RUNNING:
        # Check if there are more urls to crawl
        if TODO.empty():
            # Increment empty counter
            EMPTY_COUNTER.increment()
            # Check if other threads are producing links
            # by waiting till queue is empty
            while TODO.empty():
                # If all threads hit empty counter
                if EMPTY_COUNTER.val == THREAD_COUNT:
                    # Finish crawling
                    done_crawling()
                    return
                time.sleep(1)
            # Got a url in queue
            # Decrement counter
            EMPTY_COUNTER.decrement()
        # Queue not empty
        url = None
        try:
            if NEW_ERROR_COUNT.val >= MAX_NEW_ERRORS or \
               KNOWN_ERROR_COUNT.val >= MAX_KNOWN_ERRORS or \
               HTTP_ERROR_COUNT.val >= MAX_HTTP_ERRORS or \
               NEW_MIME_COUNT.val >= MAX_NEW_MIMES:  # If too many errors have occurred
                write_log('CRAWL', 'Too many errors have accumulated; stopping crawler.')
                done_crawling()
                break
            elif COUNTER.val >= SAVE_COUNT:  # If it's time for an autosave
                # Make sure only one thread saves files
                with save_mutex:
                    if COUNTER.val > 0:
                        try:
                            write_log('CRAWL', 'Queried {0} links.'.format(str(COUNTER.val)), worker=thread_id)
                            info_log()
                            write_log('SAVE', 'Saving files...')
                            save_files()
                            if ZIP_FILES:
                                zip_saved_files(time.time(), 'saved')
                        finally:
                            # Reset variables
                            COUNTER = Counter(0)
                            WORDS.clear()
            # Crawl the page
            else:
                try:
                    url = TODO.get(block=False)
                except queue.Empty:
                    continue
                else:
                    if check_link(url, robots_index):  # If the link is invalid
                        continue
                    links = crawl(url, thread_id)
                    for link in links:
                        # Skip empty links
                        if len(link) <= 0 or link == "/":
                            continue
                        # If link is relative, make it absolute
                        if link[0] == '/':
                            if url[-1] == '/':
                                link = url[:-1] + link
                            else:
                                link = url + link
                        TODO.put(link)
                    DONE.put(url)
                    COUNTER.increment()
                    TODO.task_done()

        # ERROR HANDLING
        except KeyboardInterrupt:  # If the user does ^C
            handle_keyboard_interrupt()

        except Exception as e:
            link = url
            write_log('CRAWL', 'An error was raised trying to process {0}'
                      .format(link), status='ERROR', worker=thread_id)
            err_mro = type(e).mro()

            if SizeError in err_mro:
                KNOWN_ERROR_COUNT.increment()
                write_log('ERROR', 'Document too large.', worker=thread_id)
                err_log(link, 'SizeError', e)

            elif OSError in err_mro:
                KNOWN_ERROR_COUNT.increment()
                write_log('ERROR', 'An OSError occurred.', worker=thread_id)
                err_log(link, 'OSError', e)

            elif str(e) == 'HTTP Error 403: Forbidden':
                write_log('ERROR', 'HTTP 403: Access Forbidden', worker=thread_id)

            elif etree.ParserError in err_mro:  # Error processing html/xml
                KNOWN_ERROR_COUNT.increment()
                write_log('ERROR', 'An XMLSyntaxError occurred. A web dev screwed up somewhere.',
                          worker=thread_id)
                err_log(link, 'XMLSyntaxError', e)

            elif requests.exceptions.SSLError in err_mro:  # Invalid SSL certificate
                KNOWN_ERROR_COUNT.increment()
                write_log('ERROR', 'An SSLError occurred. Site is using an invalid certificate',
                          worker=thread_id)
                err_log(link, 'SSLError', e)

            elif requests.exceptions.ConnectionError in err_mro:  # Error connecting to page
                KNOWN_ERROR_COUNT.increment()
                write_log('ERROR', 'A ConnectionError occurred.'
                                   'There\'s something wrong with somebody\'s network.', worker=thread_id)
                err_log(link, 'ConnectionError', e)

            elif requests.exceptions.TooManyRedirects in err_mro:  # Exceeded 30 redirects.
                KNOWN_ERROR_COUNT.increment()
                write_log('ERROR', 'A TooManyRedirects error occurred.'
                          'Page is probably part of a redirect loop.', worker=thread_id)
                err_log(link, 'TooManyRedirects', e)

            elif requests.exceptions.ContentDecodingError in err_mro:
                # Received response with content-encoding: gzip, but failed to decode it.
                KNOWN_ERROR_COUNT.increment()
                write_log('ERROR', 'A ContentDecodingError occurred.'
                          'Probably just a zip bomb, nothing to worry about.', worker=thread_id)
                err_log(link, 'ContentDecodingError', e)

            elif 'Unknown MIME type' in str(e):
                NEW_MIME_COUNT.increment()
                write_log('ERROR', 'Unknown MIME type: {0}'.format(str(e)[18:]), worker=thread_id)
                err_log(link, 'Unknown MIME', e)

            else:  # Any other error
                NEW_ERROR_COUNT.increment()
                write_log('ERROR', 'An unknown error happened. New debugging material!', worker=thread_id)
                err_log(link, 'Unknown', e)
                if RAISE_ERRORS:
                    done_crawling()
                    raise e
                else:
                    continue

            write_log('LOG', 'Saved error message and timestamp to error log file', worker=thread_id)

    write_log('CRAWL', 'Thread execution stopped.', worker=thread_id)


def check_link(item, robots_index=None):
    """
    Returns True if item is not a valid url.
    Returns False if item passes all inspections (is valid url).
    """
    # Shortest possible url being 'http://a.b', and
    # Links longer than 255 characters are usually too long for the filesystem to handle.
    if robots_index and not robots_index.is_allowed(item):
        return True
    if RESTRICT:
        if DOMAIN not in item:
            return True
    if len(item) < 10 or len(item) > 255:
        return True
    # Must be an http(s) link
    elif item[0:4] != 'http':
        return True
    elif item in copy(DONE.queue):
        return True
    return False


def check_word(word):
    """
    Returns True if word is not valid.
    Returns False if word passes all inspections (is valid).
    """
    # If word is longer than 16 characters (avg password length is ~8)
    if len(word) > 16:
        return True
    else:
        return False


def check_path(file_path):
    """
    Checks the path of a given filename to see whether it will cause errors when saving.
    Returns True if path is valid.
    Returns False if path is invalid.
    """
    if len(file_path) > 256:
        return False
    else:
        return True


def make_words(site):
    """
    Returns list of all valid words in page.
    """
    page = site.text  # Get page content
    word_list = page.split()  # Split content into lists of words, as separated by spaces
    del page
    word_list = list(set(word_list))  # Remove duplicates
    for word in word_list:
        if check_word(word):  # If word is invalid
            word_list.remove(word)  # Remove invalid word from list
    return word_list


def save_files():
    """
    Saves the TODO, done, and word lists into their respective files.
    Also logs the action to the console.
    """

    global TODO, DONE

    with open(TODO_FILE, 'w', encoding='utf-8', errors='ignore') as todoList:
        for site in copy(TODO.queue):
            try:
                todoList.write(site + '\n')  # Save TODO list
            except UnicodeError:
                continue
    write_log('SAVE', 'Saved TODO list to {0}'.format(TODO_FILE))

    with open(DONE_FILE, 'w', encoding='utf-8', errors='ignore') as done_list:
        for site in copy(DONE.queue):
            try:
                done_list.write(site + '\n')  # Save done list
            except UnicodeError:
                continue
    write_log('SAVE', 'Saved DONE list to {0}'.format(TODO_FILE))

    if SAVE_WORDS:
        update_file(WORD_FILE, WORDS.get_all(), 'words')


def make_file_path(url, ext):
    """
    Makes a valid Windows file path for a given url.
    """
    url = url.replace(ext, '')  # Remove extension from path
    for char in """/\\ *""":  # Remove illegal characters from path
        url = url.replace(char, '-')
    for char in """|:?&<>""":
        url = url.replace(char, '')
    url = url[:255] + ext  # Truncate to valid file length
    return url


def get_mime_type(page):
    """
    Extracts the Content-Type header from the headers returned by page.
    """
    try:
        doc_type = str(page.headers['content-type'])
        return doc_type
    except KeyError:  # If no Content-Type was returned, return blank
        return ''


def mime_lookup(value):
    """
    Finds the correct file extension for a MIME type using the MIME_TYPES dictionary.
    If the MIME type is blank it defaults to .html,
    and if the MIME type is not in the dictionary it raises a HeaderError.
    """
    value = value.lower()  # Reduce to lowercase
    value = value.split(';')[0]  # Remove possible encoding
    if value in MIME_TYPES:
        return MIME_TYPES[value]
    elif value == '':
        return '.html'
    else:
        raise HeaderError('Unknown MIME type: {0}'.format(value))


def save_page(url, page):
    """
    Download content of url and save to the save folder.
    """
    # Make file path
    ext = mime_lookup(get_mime_type(page))
    cropped_url = make_file_path(url, ext)
    file_path = path.join(WORKING_DIR, 'saved', '{0}'.format(cropped_url))

    # Save file
    with open(file_path, 'w', encoding='utf-8', errors='ignore') as file:
        if ext == '.html':
            file.write('''<!-- "{0}" -->
<!-- Downloaded with the spidy Web Crawler -->
<!-- https://github.com/rivermont/spidy -->
'''.format(url))
        file.write(page.text)


def update_file(file, content, file_type):
    with open(file, 'r+', encoding='utf-8', errors='ignore') as open_file:  # Open save file for reading and writing
        file_content = open_file.readlines()  # Make list of all lines in file
        contents = []
        for x in file_content:
            contents.append(x.strip())
        for item in file_content:
            content.update(item)  # Otherwise add item to content (set)
        del file_content
        for item in content:
            open_file.write('\n' + str(item))  # Write all words to file
        open_file.truncate()  # Delete everything in file beyond what has been written (old stuff)
    write_log('SAVE', 'Saved {0} {1} to {2}'.format(len(content), file_type, file))


def info_log():
    """
    Logs important information to the console and log file.
    """
    # Print to console
    write_log('LOG', 'Started at {0}'.format(START_TIME_LONG))
    write_log('LOG', 'Log location: {0}'.format(LOG_FILE_NAME))
    write_log('LOG', 'Error log location: {0}'.format(ERR_LOG_FILE_NAME))
    write_log('LOG', '{0} links in TODO'.format(TODO.qsize()))
    write_log('LOG', '{0} links in DONE'.format(DONE.qsize()))
    write_log('LOG', 'TODO/DONE: {0}'.format(TODO.qsize() / DONE.qsize()))
    write_log('LOG', '{0}/{1} new errors caught.'.format(NEW_ERROR_COUNT.val, MAX_NEW_ERRORS))
    write_log('LOG', '{0}/{1} HTTP errors encountered.'.format(HTTP_ERROR_COUNT.val, MAX_HTTP_ERRORS))
    write_log('LOG', '{0}/{1} new MIMEs found.'.format(NEW_MIME_COUNT.val, MAX_NEW_MIMES))
    write_log('LOG', '{0}/{1} known errors caught.'.format(KNOWN_ERROR_COUNT.val, MAX_KNOWN_ERRORS))


def log(message, level=logging.DEBUG):
    """
    Logs a single message to the error log file.
    Prints message verbatim, so message must be formatted correctly in the function call.

    Parameters
    ----------
    message : str
        Message to log
    level : lvl
        logging.[DEBUG, INFO, WARNING, ERROR, CRITICAL]
    """
    LOGGER.log(level, message)


def handle_invalid_input(type_='input'):
    """
    Handles an invalid user input, usually from the input() function.
    """
    LOG_FILE.write('\n[{0}] [spidy] [INPUT] [ERROR]: Please enter a valid {1}. (yes/no)'.format(get_time(), type_))
    raise SyntaxError('[{0}] [spidy] [INPUT] [ERROR]: Please enter a valid {1}. (yes/no)'.format(get_time(), type_))


def err_log(url, error1, error2):
    """
    Saves the triggering error to the log file.
    error1 is the trimmed error source.
    error2 is the extended text of the error.
    """
    LOGGER.error("\nURL: {0}\nERROR: {1}\nEXT: {2}\n\n".format(url, error1, str(error2)))


def zip_saved_files(out_file_name, directory):
    """
    Creates a .zip file in the current directory containing all contents of dir, then empties.
    """
    shutil.make_archive(str(out_file_name), 'zip', directory)  # Zips files
    shutil.rmtree(directory)  # Deletes folder
    makedirs(directory)  # Creates empty folder of same name
    write_log('SAVE', 'Zipped documents to {0}.zip'.format(out_file_name))


########
# INIT #
########

write_log('INIT', 'Creating variables...')

# Sourced mainly from https://www.iana.org/assignments/media-types/media-types.xhtml
# Added by hand after being discovered by the crawler to reduce lookup times.
MIME_TYPES = {
    'application/atom+xml': '.atom',
    'application/epub+zip': '.epub',
    'application/font-woff': '.woff',
    'application/font-woff2': '.woff2',
    'application/force-download': '.bin',  # No idea what this is so saving as .bin
    'application/gzip': '.gz',
    'application/java-archive': '.jar',
    'application/javascript': '.js',
    'application/js': '.js',  # Should be application/javascript
    'application/json': '.json',
    'application/json+oembed': '.json',
    'application/ld+json': '.jsonld',
    'application/marcxml+xml': '.mrcx',
    'application/msword': '.doc',
    'application/n-triples': '.nt',
    'application/octet-stream': '.exe',  # Sometimes .bin
    'application/ogg': '.ogx',
    'application/opensearchdescription+xml': '.osdx',
    'application/pdf': '.pdf',
    'application/postscript': '.eps',  # Also .ps
    'application/rdf+xml': '.rdf',
    'application/rsd+xml': '.rsd',
    'application/rss+xml': '.rss',
    'application/txt': '.txt',
    'application/vnd.ms-cab-compressed': '.cab',
    'application/vnd.ms-excel': '.',
    'application/vnd.ms-fontobject': '.eot',
    'application/x-endnote-refer': '.enw',
    'application/x-www-form-urlencoded': '.png',
    'application/vnd.android.package-archive': '.apk',
    'application/vnd.oasis.opendocument.text': '.odt',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
    'application/vnd.oasis.opendocument.formula-template': '.otf',
    'application/vnd.php.serialized': '.php',
    'application/x-bibtex': '.bib',
    'application/x-font-ttf': '.ttf',
    'application/x-font-woff': '.woff',
    'application/x-gzip': '.gz',
    'application/x-javascript': '.js',
    'application/x-mobipocket-ebook': '.mobi',
    'application/x-mpegurl': '.m3u8',
    'application/x-msi': '.msi',
    'application/x-research-info-systems': '.ris',
    'application/x-rss+xml': '.rss',
    'application/x-shockwave-flash': '.swf',
    'application/x-tar': '.tar.gz',  # Tarballs aren't official IANA types
    'application/xhtml+xml': '.xhtml',
    'application/xml': '.xml',
    'application/zip': '.zip',
    'audio/mpeg': '.mp3',
    'audio/mp3': '.mp3',
    'audio/x-m4a': '.m4a',
    'binary/octet-stream': '.exe',  # Should be application/octet-stream
    'font/woff': '.woff', 'font/woff2': '.woff2',
    'font/ttf': '.ttf',
    'font/otf': '.otf',
    'html': '.html',  # Incorrect
    'image/gif': '.gif',
    'image/jpeg': '.jpeg',
    'image/jpg': '.jpg',
    'image/pjpeg': '.jpg',
    'image/png': '.png',
    'image/ico': '.ico',
    'image/svg+xml': '.svg',
    'image/tiff': '.tif',
    'image/vnd.djvu': '.djvu',
    'image/vnd.microsoft.icon': '.ico',
    'image/webp': '.webp',
    'image/x-bitmap': '.xbm',
    'image/x-icon': '.ico',
    'image/x-ms-bmp': '.bmp',
    'text/calendar': '.ics',
    'text/css': '.css',
    'text/csv': '.csv',
    'text/directory': '.vcf',
    'text/html': '.html',
    'text/html,application/xhtml+xml,application/xml': '.html',  # Misunderstood 'Accept' header?
    'text/javascript': '.js',
    'text/n3': '.n3',
    'text/plain': '.txt',
    'text/turtle': '.ttl',
    'text/vnd.wap.wml': '.xml',  # or .wml
    'text/vtt': '.vtt',
    'text/x-c': '.c',
    'text/x-wiki': '.txt',  # Doesn't seem to have a filetype of its own
    'text/xml charset=utf-8': '.xml',  # Shouldn't have encoding
    'text/xml': '.xml',  # Incorrect
    'video/3gpp': '.3gp',
    'video/3gp': '.3gp',
    'video/mp4': '.mp4',
    'video/webm': '.webp',
    'video/mpeg': '.mpeg',
    'video/x-flv': '.flv',
    'vnd.ms-fontobject': '.eot'  # Incorrect
}

# User-Agent Header Strings
HEADERS = {
    'spidy': {
        'User-Agent': 'spidy Web Crawler (Mozilla/5.0; bot; +https://github.com/rivermont/spidy/)',
        'Accept-Language': 'en_US, en-US, en',
        'Accept-Encoding': 'gzip',
        'Connection': 'keep-alive'
    },
    'Chrome': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        '(KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Accept-Language': 'en_US, en-US, en',
        'Accept-Encoding': 'gzip',
        'Connection': 'keep-alive'
    },
    'Firefox': {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Accept-Language': 'en_US, en-US, en',
        'Accept-Encoding': 'gzip',
        'Connection': 'keep-alive'
    },
    'IE': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Accept-Language': 'en_US, en-US, en',
        'Accept-Encoding': 'gzip',
        'Connection': 'keep-alive'
    },
    'Edge': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        '(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
        'Accept-Language': 'en_US, en-US, en',
        'Accept-Encoding': 'gzip',
        'Connection': 'keep-alive'
    }
}

KILL_LIST = [
    # Pages that are known to cause problems with the crawler in some way
    'bhphotovideo.com/c/search',
    'scores.usaultimate.org/',
    'w3.org',
    'web.archive.org/web/'
]

# Links to start crawling if the TODO list is empty
START = ['https://en.wikipedia.org/wiki/Main_Page']

# Counter variables
COUNTER = Counter(0)
NEW_ERROR_COUNT = Counter(0)
KNOWN_ERROR_COUNT = Counter(0)
HTTP_ERROR_COUNT = Counter(0)
NEW_MIME_COUNT = Counter(0)
EMPTY_COUNTER = Counter(0)

# Empty set for word scraping
WORDS = ThreadSafeSet()
words_mutex = threading.Lock()

# Getting arguments

yes = ['y', 'yes', 'Y', 'Yes', 'True', 'true']
no = ['n', 'no', 'N', 'No', 'False', 'false']

# Initialize variables as empty that will be needed in the global scope
HEADER = {}
SAVE_COUNT, MAX_NEW_ERRORS, MAX_KNOWN_ERRORS, MAX_HTTP_ERRORS = 0, 0, 0, 0
MAX_NEW_MIMES = 0
RESPECT_ROBOTS, RESTRICT, DOMAIN = False, False, ''
USE_CONFIG, OVERWRITE, RAISE_ERRORS, ZIP_FILES, OVERRIDE_SIZE = False, False, False, False, False
SAVE_PAGES, SAVE_WORDS = False, False
TODO_FILE, DONE_FILE, WORD_FILE = '', '', ''
TODO, DONE = queue.Queue(), queue.Queue()
THREAD_COUNT = 1
THREAD_LIST = []
save_mutex = threading.Lock()
FINISHED = False
THREAD_RUNNING = True


def init():
    """
    Sets all of the variables for spidy,
    and as a result can be used for effectively resetting the crawler.
    """
    # Declare global variables
    global VERSION, START_TIME, START_TIME_LONG
    global LOG_FILE, LOG_FILE_NAME, ERR_LOG_FILE_NAME
    global HEADER, PACKAGE_DIR, WORKING_DIR, KILL_LIST
    global COUNTER, NEW_ERROR_COUNT, KNOWN_ERROR_COUNT, HTTP_ERROR_COUNT, NEW_MIME_COUNT
    global MAX_NEW_ERRORS, MAX_KNOWN_ERRORS, MAX_HTTP_ERRORS, MAX_NEW_MIMES
    global USE_CONFIG, OVERWRITE, RAISE_ERRORS, ZIP_FILES, OVERRIDE_SIZE, SAVE_WORDS, SAVE_PAGES, SAVE_COUNT
    global TODO_FILE, DONE_FILE, ERR_LOG_FILE, WORD_FILE
    global RESPECT_ROBOTS, RESTRICT, DOMAIN
    global WORDS, TODO, DONE, THREAD_COUNT

    # Getting Arguments

    if not path.exists(path.join(PACKAGE_DIR, 'config')):
        write_log('INIT', 'No config folder available.')
        USE_CONFIG = False
    else:
        write_log('INIT', 'Should spidy load settings from an available config file? (y/n):')
        input_ = input()
        if not bool(input_):
            USE_CONFIG = False
        elif input_ in yes:
            USE_CONFIG = True
        elif input_ in no:
            USE_CONFIG = False
        else:
            handle_invalid_input()

    if USE_CONFIG:
        try:
            write_log('INIT', 'Config file name:', status='INPUT')
            input_ = input()
            if input_[-4:] == '.cfg':
                file_path = path.join(PACKAGE_DIR, 'config', input_)
            else:
                file_path = path.join(PACKAGE_DIR, 'config', '{0}.cfg'.format(input_))
            write_log('INIT', 'Loading configuration settings from {0}'.format(file_path))
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line in file.readlines():
                    exec(line, globals())
        except FileNotFoundError:
            write_log('INPUT', 'Config file not found.', status='ERROR')
            raise FileNotFoundError()
        except Exception:
            write_log('INPUT', 'Please name a valid .cfg file.', status='ERROR')
            raise Exception()

    else:
        write_log('INIT', 'Please enter the following arguments. Leave blank to use the default values.')

        write_log('INIT', 'How many parallel threads should be used for crawler? (Default: 1):', status='INPUT')
        input_ = input()
        if not bool(input_):  # Use default value
            THREAD_COUNT = 1
        elif input_.isdigit():
            THREAD_COUNT = int(input_)
        else:  # Invalid input
            handle_invalid_input()

        write_log('INIT', 'Should spidy load from existing save files? (y/n) (Default: Yes):', status='INPUT')
        input_ = input()
        if not bool(input_):  # Use default value
            OVERWRITE = False
        elif input_ in yes:  # Yes
            OVERWRITE = False
        elif input_ in no:  # No
            OVERWRITE = True
        else:  # Invalid input
            handle_invalid_input()

        write_log('INIT', 'Should spidy raise NEW errors and stop crawling? (y/n) (Default: No):', status='INPUT')
        input_ = input()
        if not bool(input_):
            RAISE_ERRORS = False
        elif input_ in yes:
            RAISE_ERRORS = True
        elif input_ in no:
            RAISE_ERRORS = False
        else:
            handle_invalid_input()

        write_log('INIT', 'Should spidy save the pages it scrapes to the saved folder? (y/n) (Default: Yes):', status='INPUT')
        input_ = input()
        if not bool(input_):
            SAVE_PAGES = True
        elif input_ in yes:
            SAVE_PAGES = True
        elif input_ in no:
            SAVE_PAGES = False
        else:
            handle_invalid_input()

        if SAVE_PAGES:
            write_log('INIT', 'Should spidy zip saved documents when autosaving? (y/n) (Default: No):', status='INPUT')
            input_ = input()
            if not bool(input_):
                ZIP_FILES = False
            elif input_ in yes:
                ZIP_FILES = True
            elif input_ in no:
                ZIP_FILES = False
            else:
                handle_invalid_input()
        else:
            ZIP_FILES = False

        write_log('INIT', 'Should spidy download documents larger than 500 MB? (y/n) (Default: No):', status='INPUT')
        input_ = input()
        if not bool(input_):
            OVERRIDE_SIZE = False
        elif input_ in yes:
            OVERRIDE_SIZE = True
        elif input_ in no:
            OVERRIDE_SIZE = False
        else:
            handle_invalid_input()

        write_log('INIT', 'Should spidy scrape words and save them? (y/n) (Default: Yes):', status='INPUT')
        input_ = input()
        if not bool(input_):
            SAVE_WORDS = True
        elif input_ in yes:
            SAVE_WORDS = True
        elif input_ in no:
            SAVE_WORDS = False
        else:
            handle_invalid_input()

        write_log('INIT', 'Should spidy restrict crawling to a specific domain only? (y/n) (Default: No):',
                  status='INPUT')
        input_ = input()
        if not bool(input_):
            RESTRICT = False
        elif input_ in yes:
            RESTRICT = True
        elif input_ in no:
            RESTRICT = False
        else:
            handle_invalid_input()

        if RESTRICT:
            write_log('INIT', 'What domain should crawling be limited to? Can be subdomains, http/https, etc.',
                      status='INPUT')
            input_ = input()
            try:
                DOMAIN = input_
            except KeyError:
                handle_invalid_input('string')

        write_log('INIT', 'Should spidy respect sites\' robots.txt? (y/n) (Default: Yes):', status='INPUT')
        input_ = input()
        if not bool(input_):
            RESPECT_ROBOTS = True
        elif input_ in yes:
            RESPECT_ROBOTS = True
        elif input_ in no:
            RESPECT_ROBOTS = False
        else:
            handle_invalid_input()

        write_log('INIT', 'What HTTP browser headers should spidy imitate?', status='INPUT')
        write_log('INIT', 'Choices: spidy (default), Chrome, Firefox, IE, Edge, Custom:', status='INPUT')
        input_ = input()
        if not bool(input_):
            HEADER = HEADERS['spidy']
        elif input_.lower() == 'custom':
            write_log('INIT', 'Valid HTTP headers:', status='INPUT')
            HEADER = input()
        else:
            try:
                HEADER = HEADERS[input_]
            except KeyError:
                handle_invalid_input('browser name')

        write_log('INIT', 'Location of the TODO save file (Default: crawler_todo.txt):', status='INPUT')
        input_ = input()
        if not bool(input_):
            TODO_FILE = 'crawler_todo.txt'
        else:
            TODO_FILE = input_

        write_log('INIT', 'Location of the DONE save file (Default: crawler_done.txt):', status='INPUT')
        input_ = input()
        if not bool(input_):
            DONE_FILE = 'crawler_done.txt'
        else:
            DONE_FILE = input_

        if SAVE_WORDS:
            write_log('INIT', 'Location of the words save file (Default: crawler_words.txt):', status='INPUT')
            input_ = input()
            if not bool(input_):
                WORD_FILE = 'crawler_words.txt'
            else:
                WORD_FILE = input_
        else:
            WORD_FILE = 'None'

        write_log('INIT', 'After how many queried links should the crawler autosave? (Default: 100):', status='INPUT')
        input_ = input()
        if not bool(input_):
            SAVE_COUNT = 100
        elif not input_.isdigit():
            handle_invalid_input('integer')
        else:
            SAVE_COUNT = int(input_)

        if not RAISE_ERRORS:
            write_log('INIT', 'After how many new errors should spidy stop? (Default: 5):', status='INPUT')
            input_ = input()
            if not bool(input_):
                MAX_NEW_ERRORS = 5
            elif not input_.isdigit():
                handle_invalid_input('integer')
            else:
                MAX_NEW_ERRORS = int(input_)
        else:
            MAX_NEW_ERRORS = 1

        write_log('INIT', 'After how many known errors should spidy stop? (Default: 10):', status='INPUT')
        input_ = input()
        if not bool(input_):
            MAX_KNOWN_ERRORS = 20
        elif not input_.isdigit():
            handle_invalid_input('integer')
        else:
            MAX_KNOWN_ERRORS = int(input_)

        write_log('INIT', 'After how many HTTP errors should spidy stop? (Default: 20):', status='INPUT')
        input_ = input()
        if not bool(input_):
            MAX_HTTP_ERRORS = 50
        elif not input_.isdigit():
            handle_invalid_input('integer')
        else:
            MAX_HTTP_ERRORS = int(input_)

        write_log('INIT', 'After encountering how many new MIME types should spidy stop? (Default: 20):',
                  status='INPUT')
        input_ = input()
        if not bool(input_):
            MAX_NEW_MIMES = 10
        elif not input_.isdigit():
            handle_invalid_input('integer')
        else:
            MAX_NEW_MIMES = int(input_)

        # Remove INPUT variable from memory
        del input_

    if OVERWRITE:
        write_log('INIT', 'Creating save files...')
        for start in START:
            TODO.put(start)
        DONE = queue.Queue()
    else:
        write_log('INIT', 'Loading save files...')
        # Import saved TODO file data
        try:
            with open(TODO_FILE, 'r', encoding='utf-8', errors='ignore') as f:
                contents = f.readlines()
        except FileNotFoundError:  # If no TODO file is present
            contents = []
        for line in contents:
            TODO.put(line.strip())
        # Import saved done file data
        try:
            with open(DONE_FILE, 'r', encoding='utf-8', errors='ignore') as f:
                contents = f.readlines()
        except FileNotFoundError:  # If no DONE file is present
            contents = []
        for line in contents:
            DONE.put(line.strip())
        del contents

        # If TODO list is empty, add default starting pages
    if TODO.qsize() == 0:
        for start in START:
            TODO.put(start)


def spawn_threads(robots_index):
    """
    Spawn the crawler threads
    """
    try:
        write_log('INIT', 'Spawning {0} worker threads...'.format(THREAD_COUNT))
        for i in range(THREAD_COUNT):
            t = threading.Thread(target=crawl_worker, args=(i+1, robots_index))
            write_log('INIT', 'Starting crawl...', worker=i+1)
            t.daemon = True
            t.start()
            THREAD_LIST.append(t)
        for t in THREAD_LIST:
            t.join()
    except KeyboardInterrupt:
        handle_keyboard_interrupt()


def kill_threads():
    """
    Will terminate all running threads
    """
    global THREAD_RUNNING
    write_log('CRAWL', 'Stopping all threads...')
    THREAD_RUNNING = False


def done_crawling(keyboard_interrupt=False):
    # Make sure only one thread calls this
    with save_mutex:
        global FINISHED
        if FINISHED:
            return
        kill_threads()
        FINISHED = True
        if keyboard_interrupt:
            write_log('CRAWL', 'User performed a KeyboardInterrupt, stopping crawler.', status='ERROR')
            LOGGER.log(logging.INFO, 'User performed a KeyboardInterrupt, stopping crawler.')
        else:
            write_log('CRAWL', 'I think you\'ve managed to download the entire internet. '
                               'I guess you\'ll want to save your files...')
        save_files()
        LOG_FILE.close()


def handle_keyboard_interrupt():
    kill_threads()
    done_crawling(True)


def main():
    """
    The main function of spidy.
    """
    # Declare global variables
    global VERSION, START_TIME, START_TIME_LONG
    global LOG_FILE, LOG_FILE_NAME, ERR_LOG_FILE_NAME
    global HEADER, WORKING_DIR, KILL_LIST
    global COUNTER, NEW_ERROR_COUNT, KNOWN_ERROR_COUNT, HTTP_ERROR_COUNT, NEW_MIME_COUNT
    global MAX_NEW_ERRORS, MAX_KNOWN_ERRORS, MAX_HTTP_ERRORS, MAX_NEW_MIMES
    global USE_CONFIG, OVERWRITE, RAISE_ERRORS, ZIP_FILES, OVERRIDE_SIZE, SAVE_WORDS, SAVE_PAGES, SAVE_COUNT
    global TODO_FILE, DONE_FILE, ERR_LOG_FILE, WORD_FILE
    global RESPECT_ROBOTS, RESTRICT, DOMAIN
    global WORDS, TODO, DONE

    try:
        init()
    except Exception:
        raise SystemExit(1)

    # Create required saved/ folder
    try:
        makedirs('saved')
    except OSError:
        pass  # Assumes only OSError wil complain saved/ already exists

    # Create required files
    with open(WORD_FILE, 'w', encoding='utf-8', errors='ignore'):
        pass

    write_log('INIT', 'Successfully started spidy Web Crawler version {0}...'.format(VERSION))
    LOGGER.log(logging.INFO, 'Successfully started crawler.')

    write_log('INIT', 'Using headers: {0}'.format(HEADER))

    robots_index = RobotsIndex(RESPECT_ROBOTS, HEADER['User-Agent'])

    # Spawn threads here
    spawn_threads(robots_index)


if __name__ == '__main__':
    main()
else:
    write_log('INIT', 'Successfully imported spidy Web Crawler version {0}.'.format(VERSION))
    write_log('INIT',
              'Call `crawler.main()` to start crawling, or refer to DOCS.md to see use of specific functions.')
