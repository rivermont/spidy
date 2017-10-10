"""
spidy Web Crawler
Built by rivermont and FalconWarriorr
"""
import time
import shutil
import requests
import urllib

from os import path, makedirs
from lxml import etree
from lxml.html import iterlinks, resolve_base_href
from reppy.robots import Robots
from spidy import __version__


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
except OSError:
    pass  # Assumes only OSError wil complain if /logs already exists

LOG_FILE = open(path.join(WORKING_DIR, 'logs', 'spidy_log_{0}.txt'.format(START_TIME)),
                'w+', encoding='utf-8', errors='ignore')
LOG_FILE_NAME = path.join('logs', 'spidy_log_{0}'.format(START_TIME))


def write_log(message):
    """
    Writes message to both the console and the log file.
    NOTE: Automatically adds timestamp and `[spidy]` to message, and formats message for log appropriately.
    """
    message = '[{0}] [spidy] '.format(get_time()) + message
    print(message)
    LOG_FILE.write('\n' + message)


write_log('[INIT]: Starting spidy Web Crawler version {0}'.format(VERSION))
write_log('[INIT]: Importing required libraries...')

# Import required libraries


###########
# CLASSES #
###########

write_log('[INIT]: Creating classes...')


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


#############
# FUNCTIONS #
#############

write_log('[INIT]: Creating functions...')


def crawl(url):
    global TODO
    if not OVERRIDE_SIZE:
        try:
            # Attempt to get the size in bytes of the document
            length = int(requests.head(url).headers['Content-Length'])
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
        WORDS.update(word_list)
    try:
        # Pull out all links after resolving them using any <base> tags found in the document.
        links = [link for element, attribute, link, pos in iterlinks(resolve_base_href(page.content))]
    except etree.ParseError:
        # If the document is not HTML content this will return an empty list.
        links = []
    links = list(set(links))
    TODO += links
    DONE.append(url)
    if SAVE_PAGES:
        save_page(url, page)
    if SAVE_WORDS:
        # Announce which link was crawled
        write_log(
            '[CRAWL]: Found {0} links and {1} words on {2}'.format(len(word_list), len(links), url))
    else:
        # Announce which link was crawled
        write_log('[CRAWL]: Found {0} links on {1}'.format(len(links), url))


def init_robot_checker(respect_robots, user_agent, start_url):
    if respect_robots:
        start_path = urllib.parse.urlparse(start_url).path
        robots_url = start_url.replace(start_path, '/robots.txt')
        write_log('[INFO]: Reading robots file: {0}'.format(robots_url))
        robots = Robots.fetch(robots_url)
        checker = robots.agent(user_agent)
        return checker.allowed
    else:
        return True


def check_link(item, robots_allowed=True):
    """
    Returns True if item is not a valid url.
    Returns False if item passes all inspections (is valid url).
    """
    # Shortest possible url being 'http://a.b', and
    # Links longer than 255 characters are usually too long for the filesystem to handle.
    if not robots_allowed:
        return True
    if RESTRICT:
        if DOMAIN not in item:
            return True
    if len(item) < 10 or len(item) > 255:
        return True
    # Must be an http(s) link
    elif item[0:4] != 'http':
        return True
    elif item in DONE:
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
    with open(TODO_FILE, 'w', encoding='utf-8', errors='ignore') as todoList:
        for site in TODO:
            try:
                todoList.write(site + '\n')  # Save TODO list
            except UnicodeError:
                continue
    write_log('[LOG]: Saved TODO list to {0}'.format(TODO_FILE))

    with open(DONE_FILE, 'w', encoding='utf-8', errors='ignore') as done_list:
        for site in DONE:
            try:
                done_list.write(site + '\n')  # Save done list
            except UnicodeError:
                continue
    write_log('[LOG]: Saved done list to {0}'.format(DONE_FILE))

    if SAVE_WORDS:
        update_file(WORD_FILE, WORDS, 'words')


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
    write_log('[LOG]: Saved {0} {1} to {2}'.format(len(content), file_type, file))


def info_log():
    """
    Logs important information to the console and log file.
    """
    # Print to console
    write_log('[INFO]: Started at {0}.'.format(START_TIME_LONG))
    write_log('[INFO]: Log location: {0}'.format(LOG_FILE_NAME))
    write_log('[INFO]: Error log location: {0}'.format(ERR_LOG_FILE_NAME))
    write_log('[INFO]: {0} links in TODO.'.format(len(TODO)))
    write_log('[INFO]: {0} links in done.'.format(len(DONE)))
    write_log('[INFO]: Todo/Done: {0}'.format(len(TODO) / len(DONE)))
    write_log('[INFO]: {0}/{1} new errors caught.'.format(NEW_ERROR_COUNT, MAX_NEW_ERRORS))
    write_log('[INFO]: {0}/{1} HTTP errors encountered.'.format(HTTP_ERROR_COUNT, MAX_HTTP_ERRORS))
    write_log('[INFO]: {0}/{1} new MIMEs found.'.format(NEW_MIME_COUNT, MAX_NEW_MIMES))
    write_log('[INFO]: {0}/{1} known errors caught.'.format(KNOWN_ERROR_COUNT, MAX_KNOWN_ERRORS))


def log(message):
    """
    Logs a single message to the error log file.
    Prints message verbatim, so message must be formatted correctly in the function call.
    """
    with open(ERR_LOG_FILE, 'a', encoding='utf-8', errors='ignore') as open_file:
        open_file.write('\n\n======LOG======')  # Write opening line
        open_file.write('\nTIME: {0}'.format(get_full_time()))  # Write current time
        open_file.write(message)  # Write message
        open_file.write(LOG_END)  # Write closing line


def handle_keyboard_interrupt():
    write_log('[ERROR]: User performed a KeyboardInterrupt, stopping crawler...')
    log('\nLOG: User performed a KeyboardInterrupt, stopping crawler.')
    save_files()
    LOG_FILE.close()
    exit()


def handle_invalid_input(type_='input'):
    """
    Handles an invalid user input, usually from the input() function.
    """
    LOG_FILE.write('\n[{0}] [spidy] [ERROR]: Please enter a valid {1}. (yes/no)'.format(get_time(), type_))
    raise SyntaxError('[{0}] [spidy] [ERROR]: Please enter a valid {1}. (yes/no)'.format(get_time(), type_))


def err_log(url, error1, error2):
    """
    Saves the triggering error to the log file.
    error1 is the trimmed error source.
    error2 is the extended text of the error.
    """
    current_time = time.strftime('%H:%M:%S, %A %b %Y')  # Get the current time
    with open(ERR_LOG_FILE, 'a', encoding='utf-8', errors='ignore') as work_log:
        work_log.write('\n\n=====ERROR=====')  # Write opening line
        work_log.write('\nTIME: {0}\nURL: {1}\nERROR: {2}\nEXT: {3}'.format(current_time, url, error1, str(error2)))
        work_log.write(LOG_END)  # Write closing line


def zip_saved_files(out_file_name, directory):
    """
    Creates a .zip file in the current directory containing all contents of dir, then empties.
    """
    shutil.make_archive(str(out_file_name), 'zip', directory)  # Zips files
    shutil.rmtree(directory)  # Deletes folder
    makedirs(directory[:-1])  # Creates empty folder of same name (minus the '\ ')
    write_log('[LOG]: Zipped documents to {0}.zip'.format(out_file_name))


########
# INIT #
########

write_log('[INIT]: Creating variables...')

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

# Error log location
ERR_LOG_FILE = path.join(WORKING_DIR, 'logs', 'spidy_error_log_{0}.txt'.format(START_TIME))
ERR_LOG_FILE_NAME = path.join('logs', 'spidy_error_log_{0}.txt'.format(START_TIME))

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

# Line to print at the end of each logFile log
LOG_END = '\n======END======'

# Counter variables
COUNTER = 0
NEW_ERROR_COUNT = 0
KNOWN_ERROR_COUNT = 0
HTTP_ERROR_COUNT = 0
NEW_MIME_COUNT = 0

# Empty set for word scraping
WORDS = set([])

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
TODO, DONE = [], []


def init():
    """
    Sets all of the variables for spidy,
    and as a result can be used for effectively resetting the crawler.
    """
    # Declare global variables
    global VERSION, START_TIME, START_TIME_LONG
    global LOG_FILE, LOG_FILE_NAME, ERR_LOG_FILE_NAME
    global HEADER, PACKAGE_DIR, WORKING_DIR, KILL_LIST, LOG_END
    global COUNTER, NEW_ERROR_COUNT, KNOWN_ERROR_COUNT, HTTP_ERROR_COUNT, NEW_MIME_COUNT
    global MAX_NEW_ERRORS, MAX_KNOWN_ERRORS, MAX_HTTP_ERRORS, MAX_NEW_MIMES
    global USE_CONFIG, OVERWRITE, RAISE_ERRORS, ZIP_FILES, OVERRIDE_SIZE, SAVE_WORDS, SAVE_PAGES, SAVE_COUNT
    global TODO_FILE, DONE_FILE, ERR_LOG_FILE, WORD_FILE
    global RESPECT_ROBOTS, RESTRICT, DOMAIN
    global WORDS, TODO, DONE

    # Getting Arguments

    if not path.exists(path.join(PACKAGE_DIR, 'config')):
        write_log('[INFO]: No config folder available.')
        USE_CONFIG = False
    else:
        write_log('[INIT]: Should spidy load settings from an available config file? (y/n):')
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
            write_log('[INPUT]: Config file name:')
            input_ = input()
            if input_[-4:] == '.cfg':
                file_path = path.join(PACKAGE_DIR, 'config', input_)
            else:
                file_path = path.join(PACKAGE_DIR, 'config', '{0}.cfg'.format(input_))
            write_log('[INFO]: Loading configuration settings from {0}'.format(file_path))
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line in file.readlines():
                    exec(line, globals())
        except FileNotFoundError:
            write_log('[ERROR]: Config file not found.')
            raise FileNotFoundError()
        except Exception:
            write_log('[ERROR]: Please use a valid .cfg file.')
            raise Exception()

    else:
        write_log('[INIT]: Please enter the following arguments. Leave blank to use the default values.')

        write_log('[INPUT]: Should spidy load from existing save files? (y/n) (Default: Yes):')
        input_ = input()
        if not bool(input_):  # Use default value
            OVERWRITE = False
        elif input_ in yes:  # Yes
            OVERWRITE = False
        elif input_ in no:  # No
            OVERWRITE = True
        else:  # Invalid input
            handle_invalid_input()

        write_log('[INPUT]: Should spidy raise NEW errors and stop crawling? (y/n) (Default: No):')
        input_ = input()
        if not bool(input_):
            RAISE_ERRORS = False
        elif input_ in yes:
            RAISE_ERRORS = True
        elif input_ in no:
            RAISE_ERRORS = False
        else:
            handle_invalid_input()

        write_log('[INPUT]: Should spidy save the pages it scrapes to the saved folder? (Default: Yes):')
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
            write_log('[INPUT]: Should spidy zip saved documents when autosaving? (y/n) (Default: No):')
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

        write_log('[INPUT]: Should spidy download documents larger than 500 MB? (y/n) (Default: No):')
        input_ = input()
        if not bool(input_):
            OVERRIDE_SIZE = False
        elif input_ in yes:
            OVERRIDE_SIZE = True
        elif input_ in no:
            OVERRIDE_SIZE = False
        else:
            handle_invalid_input()

        write_log('[INPUT]: Should spidy scrape words and save them? (y/n) (Default: Yes):')
        input_ = input()
        if not bool(input_):
            SAVE_WORDS = True
        elif input_ in yes:
            SAVE_WORDS = True
        elif input_ in no:
            SAVE_WORDS = False
        else:
            handle_invalid_input()

        write_log('[INPUT]: Should spidy restrict crawling to a specific domain only? (y/n) (Default: No):')
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
            write_log('[INPUT]: What domain should crawling be limited to? Can be subdomains, http/https, etc.')
            input_ = input()
            try:
                DOMAIN = input_
            except KeyError:
                handle_invalid_input('string')

        write_log('[INPUT]: Should spidy respect sites\' robots.txt? (y/n) (Default: Yes):')
        input_ = input()
        if not bool(input_):
            RESPECT_ROBOTS = True
        elif input_ in yes:
            RESPECT_ROBOTS = True
        elif input_ in no:
            RESPECT_ROBOTS = False
        else:
            handle_invalid_input()

        write_log('[INPUT]: What HTTP browser headers should spidy imitate?')
        write_log('[INPUT]: Choices: spidy (default), Chrome, Firefox, IE, Edge, Custom:')
        input_ = input()
        if not bool(input_):
            HEADER = HEADERS['spidy']
        elif input_.lower() == 'custom':
            write_log('[INPUT]: Valid HTTP Headers:')
            HEADER = input()
        else:
            try:
                HEADER = HEADERS[input_]
            except KeyError:
                handle_invalid_input('browser name')

        write_log('[INPUT]: Location of the TODO save file (Default: crawler_todo.txt):')
        input_ = input()
        if not bool(input_):
            TODO_FILE = 'crawler_todo.txt'
        else:
            TODO_FILE = input_

        write_log('[INPUT]: Location of the done save file (Default: crawler_done.txt):')
        input_ = input()
        if not bool(input_):
            DONE_FILE = 'crawler_done.txt'
        else:
            DONE_FILE = input_

        if SAVE_WORDS:
            write_log('[INPUT]: Location of the word save file: (Default: crawler_words.txt):')
            input_ = input()
            if not bool(input_):
                WORD_FILE = 'crawler_words.txt'
            else:
                WORD_FILE = input_
        else:
            WORD_FILE = 'None'

        write_log('[INPUT]: After how many queried links should spidy autosave? (default 100):')
        input_ = input()
        if not bool(input_):
            SAVE_COUNT = 100
        elif not input_.isdigit():
            handle_invalid_input('integer')
        else:
            SAVE_COUNT = int(input_)

        if not RAISE_ERRORS:
            write_log('[INPUT]: After how many new errors should spidy stop? (default: 5):')
            input_ = input()
            if not bool(input_):
                MAX_NEW_ERRORS = 5
            elif not input_.isdigit():
                handle_invalid_input('integer')
            else:
                MAX_NEW_ERRORS = int(input_)
        else:
            MAX_NEW_ERRORS = 1

        write_log('[INPUT]: After how many known errors should spidy stop? (default: 10):')
        input_ = input()
        if not bool(input_):
            MAX_KNOWN_ERRORS = 20
        elif not input_.isdigit():
            handle_invalid_input('integer')
        else:
            MAX_KNOWN_ERRORS = int(input_)

        write_log('[INPUT]: After how many HTTP errors should spidy stop? (default: 20):')
        input_ = input()
        if not bool(input_):
            MAX_HTTP_ERRORS = 50
        elif not input_.isdigit():
            handle_invalid_input('integer')
        else:
            MAX_HTTP_ERRORS = int(input_)

        write_log('[INPUT]: After encountering how many MIME types should spidy stop? (default: 20):')
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
        write_log('[INIT]: Creating save files...')
        TODO = START
        DONE = []
    else:
        write_log('[INIT]: Loading save files...')
        # Import saved TODO file data
        try:
            with open(TODO_FILE, 'r', encoding='utf-8', errors='ignore') as f:
                contents = f.readlines()
        except FileNotFoundError:  # If no TODO file is present
            contents = []
        for line in contents:
            TODO.append(line.strip())
        # Import saved done file data
        try:
            with open(DONE_FILE, 'r', encoding='utf-8', errors='ignore') as f:
                contents = f.readlines()
        except FileNotFoundError:  # If no DONE file is present
            contents = []
        for line in contents:
            DONE.append(line.strip())
        del contents

        # If TODO list is empty, add default starting pages
    if len(TODO) == 0:
        TODO += START


def main():
    """
    The main function of spidy.
    """
    # Declare global variables
    global VERSION, START_TIME, START_TIME_LONG
    global LOG_FILE, LOG_FILE_NAME, ERR_LOG_FILE_NAME
    global HEADER, WORKING_DIR, KILL_LIST, LOG_END
    global COUNTER, NEW_ERROR_COUNT, KNOWN_ERROR_COUNT, HTTP_ERROR_COUNT, NEW_MIME_COUNT
    global MAX_NEW_ERRORS, MAX_KNOWN_ERRORS, MAX_HTTP_ERRORS, MAX_NEW_MIMES
    global USE_CONFIG, OVERWRITE, RAISE_ERRORS, ZIP_FILES, OVERRIDE_SIZE, SAVE_WORDS, SAVE_PAGES, SAVE_COUNT
    global TODO_FILE, DONE_FILE, ERR_LOG_FILE, WORD_FILE
    global RESPECT_ROBOTS, RESTRICT, DOMAIN
    global WORDS, TODO, DONE

    try:
        init()
    except Exception as error:
        raise SystemExit(1) 

    # Create required saved/ folder
    try:
        makedirs('saved')
    except OSError:
        pass  # Assumes only OSError wil complain saved/ already exists

    # Create required files
    with open(WORD_FILE, 'w', encoding='utf-8', errors='ignore'):
        pass

    write_log('[INIT]: Successfully started spidy Web Crawler version {0}...'.format(VERSION))
    log('LOG: Successfully started crawler.')

    robots_allowed = init_robot_checker(RESPECT_ROBOTS, HEADER['User-Agent'], TODO[0])

    write_log('[INFO]: TODO first value: {0}'.format(TODO[0]))

    write_log('[INFO]: Using headers: {0}'.format(HEADER))

    while len(TODO) != 0:  # While there are links to check
        try:
            if NEW_ERROR_COUNT >= MAX_NEW_ERRORS or \
               KNOWN_ERROR_COUNT >= MAX_KNOWN_ERRORS or \
               HTTP_ERROR_COUNT >= MAX_HTTP_ERRORS or \
               NEW_MIME_COUNT >= MAX_NEW_MIMES:  # If too many errors have occurred
                write_log('[INFO]: Too many errors have accumulated, stopping crawler.')
                save_files()
                exit()
            elif COUNTER >= SAVE_COUNT:  # If it's time for an autosave
                try:
                    write_log('[INFO]: Queried {0} links.'.format(str(COUNTER)))
                    info_log()
                    write_log('[INFO]: Saving files...')
                    save_files()
                    if ZIP_FILES:
                        zip_saved_files(time.time(), 'saved')
                finally:
                    # Reset variables
                    COUNTER = 0
                    WORDS.clear()
            elif check_link(TODO[0], robots_allowed):  # If the link is invalid
                del TODO[0]
            # Crawl the page
            else:
                crawl(TODO[0])
                del TODO[0]  # Remove crawled link from TODO list
                COUNTER += 1

        # ERROR HANDLING
        except KeyboardInterrupt:  # If the user does ^C
            handle_keyboard_interrupt()

        except Exception as e:
            link = TODO[0].encode('utf-8', 'ignore')
            write_log('[INFO]: An error was raised trying to process {0}'.format(link))
            err_mro = type(e).mro()

            if SizeError in err_mro:
                KNOWN_ERROR_COUNT += 1
                write_log('[ERROR]: Document too large.')
                err_log(link, 'SizeError', e)

            elif OSError in err_mro:
                KNOWN_ERROR_COUNT += 1
                write_log('[ERROR]: An OSError occurred.')
                err_log(link, 'OSError', e)

            elif str(e) == 'HTTP Error 403: Forbidden':
                write_log('[ERROR]: HTTP 403: Access Forbidden.')

            elif etree.ParserError in err_mro:  # Error processing html/xml
                KNOWN_ERROR_COUNT += 1
                write_log('[ERROR]: An XMLSyntaxError occurred. Web dev screwed up somewhere.')
                err_log(link, 'XMLSyntaxError', e)

            elif requests.exceptions.SSLError in err_mro:  # Invalid SSL certificate
                KNOWN_ERROR_COUNT += 1
                write_log('[ERROR]: An SSLError occurred. Site is using an invalid certificate.')
                err_log(link, 'SSLError', e)

            elif requests.exceptions.ConnectionError in err_mro:  # Error connecting to page
                KNOWN_ERROR_COUNT += 1
                write_log('[ERROR]: A ConnectionError occurred. There\'s something wrong with somebody\'s network.')
                err_log(link, 'ConnectionError', e)

            elif requests.exceptions.TooManyRedirects in err_mro:  # Exceeded 30 redirects.
                KNOWN_ERROR_COUNT += 1
                write_log('[ERROR]: A TooManyRedirects error occurred. Page is probably part of a redirect loop.')
                err_log(link, 'TooManyRedirects', e)

            elif requests.exceptions.ContentDecodingError in err_mro:
                # Received response with content-encoding: gzip, but failed to decode it.
                KNOWN_ERROR_COUNT += 1
                write_log('[ERROR]: A ContentDecodingError occurred. Probably just a zip bomb, nothing to worry about.')
                err_log(link, 'ContentDecodingError', e)

            elif 'Unknown MIME type' in str(e):
                NEW_MIME_COUNT += 1
                write_log('[ERROR]: Unknown MIME type: {0}'.format(str(e)[18:]))
                err_log(link, 'Unknown MIME', e)

            else:  # Any other error
                NEW_ERROR_COUNT += 1
                write_log('[ERROR]: An unknown error happened. New debugging material!')
                err_log(link, 'Unknown', e)
                if RAISE_ERRORS:
                    LOG_FILE.close()
                    save_files()
                    raise e
                else:
                    continue

            write_log('[LOG]: Saved error message and timestamp to error log file.')
            del TODO[0]
            COUNTER += 1
        finally:
            try:
                TODO = list(set(TODO))  # Removes duplicates and shuffles links so trees don't form.
                # For debugging purposes; uncomment to check one link and then stop:
                # handle_keyboard_interrupt()
                # exit()
            except KeyboardInterrupt:
                handle_keyboard_interrupt()

    write_log('[INFO]: I think you\'ve managed to download the internet. I guess you\'ll want to save your files...')
    save_files()
    LOG_FILE.close()


if __name__ == '__main__':
    main()
else:
    write_log('[INIT]: Successfully imported spidy Web Crawler.')
    write_log('[INIT]: Call `crawler.main()` to start crawling, or refer to docs.md to see use of specific functions.')
