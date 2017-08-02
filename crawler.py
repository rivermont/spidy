'''
spidy Web Crawler
Built by rivermont and FalconWarriorr
'''
VERSION = '1.0'

##########
# IMPORT #
##########

# Time statements.
# This is done before anything else to enable timestamp logging at every step
import time as t

START_TIME = int(t.time())


def get_time():
	return t.strftime('%H:%M:%S')
START_TIME_LONG = get_time()


def get_full_time():
	return t.strftime('%H:%M:%S, %A %b %Y')


# Get current working directory of spidy
from os import path

CRAWLER_DIR = path.dirname(path.realpath(__file__))

# Open log file for logging
LOG_FILE = open('{0}/logs/spidy_log_{1}.txt'.format(CRAWLER_DIR, START_TIME), 'w+')
LOG_FILE_NAME = 'logs/spidy_log_{0}'.format(START_TIME)


def write_log(message):
	'''
	Writes message to both the console and the log file.
	NOTE: Automatically adds timestamp and `[spidy]` to message, and formats message for log appropriately.
	'''
	message = '[{0}] [spidy] '.format(get_time()) + message
	print(message)
	LOG_FILE.write('\n' + message)

write_log('[INIT]: Starting spidy Web Crawler version {0}'.format(VERSION))
write_log('[INIT]: Importing required libraries...')

# Import required libraries
import requests
import shutil
import sys
from lxml import html, etree
from os import makedirs

###########
# CLASSES #
###########

write_log('[INIT]: Creating classes...')


class HeaderError(Exception):
	'''
	Raised when there's a problem deciphering returned HTTP headers.
	'''
	pass


#############
# FUNCTIONS #
#############

write_log('[INIT]: Creating functions...')


def check_link(item):
	'''
	Returns True if item is not a valid url.
	Returns False if item passes all inspections (is valid url).
	'''
	# Shortest possible url being 'http://a.b', and
	# Links longer than 255 characters are usually useless or full of foreign characters,
	# and will also cause problems when saving.
	if len(item) < 10 or len(item) > 255:
		return True
	# Must be an http(s) link
	elif item[0:4] != 'http':
		return True
	elif item in DONE:
		return True
	else:
		for bad_link in KILL_LIST:
			if bad_link in item:
				return True
	return False


def check_word(word):
	'''
	Returns True if word is not valid.
	Returns False if word passes all inspections (is valid).
	'''
	# If word is longer than 16 characters (avg password length is ~8)
	if len(word) > 16:
		return True
	else:
		return False


def check_path(file_path):
	'''
	Checks the path of a given filename to see whether it will cause errors when saving.
	Returns True if path is valid.
	Returns False if path is invalid.
	'''
	if len(file_path) > 256:
		return False
	else:
		return True


def make_words(site):
	'''
	Returns list of all valid words in page.
	'''
	page = str(site.content)  # Get page content
	word_list = page.split()  # Split content into lists of words, as separated by spaces
	del page
	word_list = list(set(word_list))  # Remove duplicates
	for word in word_list:
		if check_word(word):  # If word is invalid
			word_list.remove(word)  # Remove invalid word from list
	return word_list


def save_files(word_list):
	'''
	Saves the TODO, done, word, and bad lists into their respective files.
	Also logs the action to the console.
	'''
	with open(TODO_FILE, 'w') as todoList:
		for site in TODO:
			try:
				todoList.write(site + '\n')  # Save TODO list
			except UnicodeError:
				continue
	write_log('[LOG]: Saved TODO list to {0}'.format(TODO_FILE))

	with open(DONE_FILE, 'w') as done_list:
		for site in DONE:
			try:
				done_list.write(site + '\n')  # Save done list
			except UnicodeError:
				continue
	write_log('[LOG]: Saved done list to {0}'.format(DONE_FILE))

	if SAVE_WORDS:
		update_file(WORD_FILE, word_list, 'words')

	update_file(BAD_FILE, BAD_LINKS, 'bad links')


def make_file_path(url, ext):
	'''
	Makes a valid Windows file path for a url.
	'''
	url = url.replace(ext, '')  # Remove extension from path
	for char in '''/\ *''':  # Remove illegal characters from path
		url = url.replace(char, '-')
	for char in '''|:?&<>''':
		url = url.replace(char, '')
	url = url[:255]  # Truncate to valid file length
	return url


def get_mime_type(page):
	'''
	Extracts the Content-Type header from the headers returned by page.
	'''
	try:
		doc_type = str(page.headers['content-type'])
		return doc_type
	except KeyError:  # If no Content-Type was returned, return blank
		return ''


def mime_lookup(value):
	'''
	Finds the correct file extension for a MIME type using the MIME_TYPES dictionary.
	If the MIME type is blank it defaults to .html,
	and if the MIME type is not in the dictionary it raises a HeaderError.
	'''
	value = value.lower()  # Reduce to lowercase
	value = value.split(';')[0]  # Remove possible encoding
	if value in MIME_TYPES:
		return MIME_TYPES[value]
	elif value == '':
		return '.html'
	else:
		raise HeaderError('Unknown MIME type: {0}'.format(value))


def save_page(url, page):
	'''
	Download content of url and save to the save folder.
	'''
	# Make file path
	ext = mime_lookup(get_mime_type(page))
	cropped_url = make_file_path(url, ext)
	path = '{0}/saved/{1}{2}'.format(CRAWLER_DIR, cropped_url, ext)

	# Save file
	with open(path, 'wb+') as file:
		file.write(page.content)


def update_file(file, content, filetype):
	with open(file, 'r+') as f:  # Open save file for reading and writing
		file_content = f.readlines()  # Make list of all lines in file
		file_content = [x.strip() for x in file_content]
		for item in file_content:
			content.update(item)  # Otherwise add item to content (set)
		del file_content
		for item in content:
			f.write('\n' + str(item))  # Write all words to file
		f.truncate()  # Delete everything in file beyond what has been written (old stuff)
	write_log('[LOG]: Saved {0} {1} to {2}'.format(len(content), filetype, file))


def info_log():
	'''
	Logs important information to the console and log file.
	'''
	# Print to console
	write_log('[INFO]: Started at {0}.'.format(START_TIME_LONG))
	write_log('[INFO]: Log location: {0}'.format(LOG_FILE_NAME))
	write_log('[INFO]: Error log location: {0}'.format(ERR_LOG_FILE_NAME))
	write_log('[INFO]: {0} links in TODO.'.format(len(TODO)))
	write_log('[INFO]: {0} links in done.'.format(len(DONE)))
	write_log('[INFO]: {0}/{1} new errors caught.'.format(NEW_ERROR_COUNT, MAX_NEW_ERRORS))
	write_log('[INFO]: {0}/{1} HTTP errors encountered.'.format(HTTP_ERROR_COUNT, MAX_HTTP_ERRORS))
	write_log('[INFO]: {0}/{1} new MIMEs found.'.format(NEW_MIME_COUNT, MAX_NEW_MIMES))
	write_log('[INFO]: {0}/{1} known errors caught.'.format(KNOWN_ERROR_COUNT, MAX_KNOWN_ERRORS))


def log(message):
	'''
	Logs a single message to the error log file.
	Prints message verbatim, so message must be formatted correctly in the function call.
	'''
	with open(ERR_LOG_FILE, 'a') as log:
		log.write('\n\n======LOG======')  # Write opening line
		log.write('\nTIME: {0}'.format(get_full_time()))  # Write current time
		log.write(message)  # Write message
		log.write(LOG_END)  # Write closing line


def handle_keyboard_interrupt():
	write_log('[ERR]: User performed a KeyboardInterrupt, stopping crawler...')
	log('\nLOG: User performed a KeyboardInterrupt, stopping crawler.')
	save_files(WORDS)
	LOG_FILE.close()
	sys.exit()


def err_log(url, error1, error2):
	'''
	Saves the triggering error to the log file.
	error1 is the trimmed error source.
	error2 is the extended text of the error.
	'''
	time = t.strftime('%H:%M:%S, %A %b %Y')  # Get the current time
	with open(ERR_LOG_FILE, 'a') as work_log:
		work_log.write('\n\n=====ERROR=====')  # Write opening line
		work_log.write('\nTIME: {0}\nURL: {1}\nERROR: {2}\nEXT: {3}'.format(time, url, error1, str(error2)))
		work_log.write(LOG_END)  # Write closing line


def zip_files(out_file_name, directory):
	'''
	Creates a .zip file in the current directory containing all contents of dir, then empties.
	'''
	shutil.make_archive(str(out_file_name), 'zip', directory)  # Zips files
	shutil.rmtree(directory)  # Deletes folder
	makedirs(directory[:-1])  # Creates empty folder of same name (minus the '/')
	write_log('[LOG]: Zipped documents to {0}.zip'.format(out_file_name))


########
# INIT #
########

write_log('[INIT]: Creating variables...')

# Sourced mainly from https://www.iana.org/assignments/media-types/media-types.xhtml
# Added by hand after being found by the crawler to reduce lookup times.
MIME_TYPES = {
	'application/atom+xml': '.atom',
	'application/epub+zip': '.epub',
	'application/font-woff': '.woff',
	'application/font-woff2': '.woff2',
	'application/java-archive': '.jar',
	'application/javascript': '.js',
	'application/json': '.json',
	'application/js': '.js',  # Should be application/javascript
	'application/marcxml+xml': '.mrcx',
	'application/msword': '.doc',
	'application/gzip': '.gz',
	'application/n-triples': '.nt',
	'application/octet-stream': '.exe',  # Sometimes .bin
	'text/xml charset=utf-8': '.xml',  # Shouldn't have encoding
	'application/ogg': '.ogx',
	'application/opensearchdescription+xml': '.osdx',
	'application/pdf': '.pdf',
	'application/rdf+xml': '.rdf',
	'application/rsd+xml': '.rsd',
	'application/rss+xml': '.rss',
	'application/vnd.ms-cab-compressed': '.cab',
	'application/vnd.ms-fontobject': '.eot',
	'application/vnd.ms-excel': '.',
	'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
	'application/vnd.oasis.opendocument.text': '.odt',
	'text/html,application/xhtml+xml,application/xml': '.html',  # Misunderstood 'Accept' header?
	'application/vnd.php.serialized': '.php',
	'application/x-bibtex': '.bib',  # I think
	'application/x-font-woff': '.woff',
	'application/x-gzip': '.gz',
	'application/x-javascript': '.js',
	'application/x-mobipocket-ebook': '.mobi',
	'application/x-msi': '.msi',
	'application/x-research-info-systems': '.ris',
	'application/x-rss+xml': '.rss',
	'application/x-shockwave-flash': '.swf',
	'application/x-tar': '.tar.gz',  # Tarballs aren't official IANA types
	'application/xhtml+xml': '.xhtml',
	'application/xml': '.xml',
	'application/zip': '.zip',
	'audio/mpeg': '.mp3',
	'font/woff': '.woff', 'font/woff2': '.woff2',
	'html': '.html',  # Incorrect
	'image/gif': '.gif',
	'image/jpeg': '.jpeg',
	'image/jpg': '.jpg',
	'image/png': '.png',
	'image/svg+xml': '.svg',
	'image/tiff': '.tif',
	'image/vnd.djvu': '.djvu',
	'image/vnd.microsoft.icon': '.ico',
	'image/webp': '.webp',
	'image/x-icon': '.ico',
	'image/x-ms-bmp': '.bmp',
	'text/calendar': '.ics',
	'text/css': '.css',
	'text/html': '.html',
	'text/javascript': '.js',
	'text/n3': '.n3',
	'text/plain': '.txt',
	'text/turtle': '.ttl',
	'text/vtt': '.vtt',
	'text/vnd.wap.wml': '.xml',  # or .wml
	'text/x-c': '.c',
	'text/xml': '.xml',  # Incorrect
	'video/mp4': '.mp4',
	'video/webm': '.webp',
	'vnd.ms-fontobject': '.eot',  # Incorrect
}

# Error log location
ERR_LOG_FILE = '{0}/logs/spidy_error_log_{1}.txt'.format(CRAWLER_DIR, START_TIME)
ERR_LOG_FILE_NAME = 'logs/spidy_error_log_{0}.txt'.format(START_TIME)

# User-Agent Header Strings
HEADERS = {
	'spidy': {
		'User-Agent': 'spidy Web Crawler (Mozilla/5.0; bot; +https://github.com/rivermont/spidy/)',
		'Accept-Language': 'en_US, en-US, en',
		'Accept-Encoding': 'gzip',
		'Connection': 'keep-alive'
	},
	'Chrome': {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
		'Accept-Language': 'en_US, en-US, en',
		'Accept-Encoding': 'gzip',
		'Connection': 'keep-alive'
	},
	# 'Firefox': {
	# 'User-Agent': '?'
	# 'Accept-Language': 'en_US, en-US, en',
	# 'Accept-Encoding': 'gzip',
	# 'Connection': 'keep-alive'
	# }
	'IE': {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
		'Accept-Language': 'en_US, en-US, en',
		'Accept-Encoding': 'gzip',
		'Connection': 'keep-alive'
	},
	'Edge': {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
		'Accept-Language': 'en_US, en-US, en',
		'Accept-Encoding': 'gzip',
		'Connection': 'keep-alive'
	}
}

KILL_LIST = [
	# Pages that are known to cause problems with the crawler in some way
	'scores.usaultimate.org/',
	'w3.org',
	'web.archive.org/web/'
]

# Links to start crawling if the TODO list is empty
START = ['https://en.wikipedia.org/wiki/Main_Page']

# Empty set for error-causing links
BAD_LINKS = set([])

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

try:
	path = 'config/' + sys.argv[1] + '.cfg'
	write_log('[INFO]: Using configuration settings from {0}'.format(path))
	with open(path, 'r') as f:
		for line in f:
			exec(line)
	GET_ARGS = False
except FileNotFoundError:
	LOG_FILE.write('\n[{0}] [spidy] [ERR]: Please use a valid .cfg file.'.format(get_time()))
	raise FileNotFoundError('[{0}] [spidy] [ERR]: Please use a valid .cfg file.'.format(get_time()))
except IndexError:
	GET_ARGS = True

if GET_ARGS:
	write_log('[INIT]: Please enter the following arguments. Leave blank to use the default values.')

	INPUT = input('[{0}] [spidy] [INPUT]: Should spidy load from existing save files? (y/n) (Default: Yes): '.format(get_time()))
	LOG_FILE.write('\n[{0}] [spidy] [INPUT]: Should spidy load from existing save files? (y/n) (Default: Yes): '.format(get_time()))
	if not bool(INPUT):  # Use default value
		OVERWRITE = False
	elif INPUT in yes:  # Yes
		OVERWRITE = False
	elif INPUT in no:  # No
		OVERWRITE = True
	else:  # Invalid input
		LOG_FILE.write('\n[{0}] [spidy] [ERR]: Please enter a valid input. (yes/no)'.format(get_time()))
		raise SyntaxError('[{0}] [spidy] [ERR]: Please enter a valid input. (yes/no)'.format(get_time()))

	INPUT = input('[{0}] [spidy] [INPUT]: Should spidy raise NEW errors and stop crawling? (y/n) (Default: No): '.format(get_time()))
	LOG_FILE.write('\n[{0}] [spidy] [INPUT]: Should spidy raise NEW errors and stop crawling? (y/n) (Default: No): '.format(get_time()))
	if not bool(INPUT):
		RAISE_ERRORS = False
	elif INPUT in yes:
		RAISE_ERRORS = True
	elif INPUT in no:
		RAISE_ERRORS = False
	else:
		LOG_FILE.write('\n[{0}] [spidy] [ERR]: Please enter a valid input. (yes/no)'.format(get_time()))
		raise SyntaxError('[{0}] [spidy] [ERR]: Please enter a valid input. (yes/no)'.format(get_time()))

	INPUT = input('[{0}] [spidy] [INPUT]: Should spidy save the pages it scrapes to the saved folder? (Default: Yes): '.format(get_time()))
	LOG_FILE.write('\n[{0}] [spidy] [INPUT]: Should spidy save the pages it scrapes to the saved folder? (Default: Yes): '.format(get_time()))
	if not bool(INPUT):
		SAVE_PAGES = True
	elif INPUT in yes:
		SAVE_PAGES = True
	elif INPUT in no:
		SAVE_PAGES = False
	else:
		LOG_FILE.write('\n[{0}] [spidy] [ERR]: Please enter a valid input. (yes/no)'.format(get_time()))
		raise SyntaxError('[{0}] [spidy] [ERR]: Please enter a valid input. (yes/no)'.format(get_time()))

	if SAVE_PAGES:
		INPUT = input('[{0}] [spidy] [INPUT]: Should spidy zip saved documents when autosaving? (y/n) (Default: No): '.format(get_time()))
		LOG_FILE.write('\n[{0}] [spidy] [INPUT]: Should spidy zip saved documents when autosaving? (y/n) (Default: No): '.format(get_time()))
		if not bool(INPUT):
			ZIP_FILES = False
		elif INPUT in yes:
			ZIP_FILES = True
		elif INPUT in no:
			ZIP_FILES = False
		else:
			LOG_FILE.write('\n[{0}] [spidy] [ERR]: Please enter a valid input. (yes/no)'.format(get_time()))
			raise SyntaxError('[{0}] [spidy] [ERR]: Please enter a valid input. (yes/no)'.format(get_time()))
	else:
		ZIP_FILES = False

	INPUT = input('[{0}] [spidy] [INPUT]: Should spidy scrape words and save them? (y/n) (Default: Yes): '.format(get_time()))
	LOG_FILE.write('\n[{0}] [spidy] [INPUT]: Should spidy scrape words and save them? (y/n) (Default: Yes): '.format(get_time()))
	if not bool(INPUT):
		SAVE_WORDS = True
	elif INPUT in yes:
		SAVE_WORDS = True
	elif INPUT in no:
		SAVE_WORDS = False
	else:
		LOG_FILE.write('\n[{0}] [spidy] [ERR]: Please enter a valid input. (yes/no)'.format(get_time()))
		raise SyntaxError('[{0}] [spidy] [ERR]: Please enter a valid input. (yes/no)'.format(get_time()))

	INPUT = input('[{0}] [spidy] [INPUT]: What browser headers should spidy use?\n[{0}] [spidy] [INPUT]: Choices: spidy (default), Chrome, IE, Edge: '.format(get_time()))
	LOG_FILE.write('\n[{0}] [spidy] [INPUT]: What browser headers should spidy use?\n[{0}] [spidy] [INPUT]: Choices: spidy (default), Chrome, IE, Edge: '.format(get_time()))
	if not bool(INPUT):
		HEADER = HEADERS['spidy']
	else:
		try:
			HEADER = HEADERS[INPUT]
		except KeyError:
			LOG_FILE.write('\n[{0}] [spidy] [ERR]: Invalid browser name.'.format(get_time()))
			raise KeyError('[{0}] [spidy] [ERR]: Invalid browser name.'.format(get_time()))

	INPUT = input('[{0}] [spidy] [INPUT]: Location of the TODO save file (Default: crawler_todo.txt): '.format(get_time()))
	LOG_FILE.write('\n[{0}] [spidy] [INPUT]: Location of the TODO save file (Default: crawler_todo.txt): '.format(get_time()))
	if not bool(INPUT):
		TODO_FILE = 'crawler_todo.txt'
	else:
		TODO_FILE = INPUT

	INPUT = input('[{0}] [spidy] [INPUT]: Location of the done save file (Default: crawler_done.txt): '.format(get_time()))
	LOG_FILE.write('\n[{0}] [spidy] [INPUT]: Location of the done save file (Default: crawler_done.txt): '.format(get_time()))
	if not bool(INPUT):
		DONE_FILE = 'crawler_done.txt'
	else:
		DONE_FILE = INPUT

	if SAVE_WORDS:
		INPUT = input('[{0}] [spidy] [INPUT]: Location of the word save file: (Default: crawler_words.txt): '.format(get_time()))
		LOG_FILE.write('\n[{0}] [spidy] [INPUT]: Location of the word save file: (Default: crawler_words.txt): '.format(get_time()))
		if not bool(INPUT):
			WORD_FILE = 'crawler_words.txt'
		else:
			WORD_FILE = INPUT
	else:
		WORD_FILE = 'None'

	INPUT = input('[{0}] [spidy] [INPUT]: Location of the bad link save file (Default: crawler_bad.txt): '.format(get_time()))
	LOG_FILE.write('\n[{0}] [spidy] [INPUT]: Location of the bad link save file (Default: crawler_bad.txt): '.format(get_time()))
	if not bool(INPUT):
		BAD_FILE = 'crawler_bad.txt'
	else:
		BAD_FILE = INPUT

	INPUT = input('[{0}] [spidy] [INPUT]: After how many queried links should spidy autosave? (default 100): '.format(get_time()))
	LOG_FILE.write('\n[{0}] [spidy] [INPUT]: After how many queried links should spidy autosave? (default 100): '.format(get_time()))
	if not bool(INPUT):
		SAVE_COUNT = 100
	elif not INPUT.isdigit():
		LOG_FILE.write('\n[{0}] [spidy] [ERR]: Please enter a valid integer.'.format(get_time()))
		raise SyntaxError('[{0}] [spidy] [ERR]: Please enter a valid integer.'.format(get_time()))
	else:
		SAVE_COUNT = int(INPUT)

	if not RAISE_ERRORS:
		INPUT = input('[{0}] [spidy] [INPUT]: After how many new errors should spidy stop? (default: 5): '.format(get_time()))
		LOG_FILE.write('\n[{0}] [spidy] [INPUT]: After how many new errors should spidy stop? (default: 5): '.format(get_time()))
		if not bool(INPUT):
			MAX_NEW_ERRORS = 5
		elif not INPUT.isdigit():
			LOG_FILE.write('\n[{0}] [spidy] [ERR]: Please enter a valid integer.'.format(get_time()))
			raise SyntaxError('[{0}] [spidy] [ERR]: Please enter a valid integer.'.format(get_time()))
		else:
			MAX_NEW_ERRORS = int(INPUT)
	else:
		MAX_NEW_ERRORS = 1

	INPUT = input('[{0}] [spidy] [INPUT]: After how many known errors should spidy stop? (default: 10): '.format(get_time()))
	LOG_FILE.write('\n[{0}] [spidy] [INPUT]: After how many known errors should spidy stop? (default: 10): '.format(get_time()))
	if not bool(INPUT):
		MAX_KNOWN_ERRORS = 20
	elif not INPUT.isdigit():
		LOG_FILE.write('\n[{0}] [spidy] [ERR]: Please enter a valid integer.'.format(get_time()))
		raise SyntaxError('[{0}] [spidy] [ERR]: Please enter a valid integer.'.format(get_time()))
	else:
		MAX_KNOWN_ERRORS = int(INPUT)

	INPUT = input('[{0}] [spidy] [INPUT]: After how many HTTP errors should spidy stop? (default: 20): '.format(get_time()))
	LOG_FILE.write('\n[{0}] [spidy] [INPUT]: After how many HTTP errors should spidy stop? (default: 20): '.format(get_time()))
	if not bool(INPUT):
		MAX_HTTP_ERRORS = 50
	elif not INPUT.isdigit():
		LOG_FILE.write('\n[{0}] [spidy] [ERR]: Please enter a valid integer.'.format(get_time()))
		raise SyntaxError('[{0}] [spidy] [ERR]: Please enter a valid integer.'.format(get_time()))
	else:
		MAX_HTTP_ERRORS = int(INPUT)

	INPUT = input('[{0}] [spidy] [INPUT]: After how many unrecognized MIME types should spidy stop? (default: 10)'.format(get_time()))
	LOG_FILE.write('[{0}] [spidy] [INPUT]: After how many unrecognized MIME types should spidy stop? (default: 10)'.format(get_time()))
	if not bool(INPUT):
		MAX_NEW_MIMES = 10
	elif not INPUT.isdigit():
		LOG_FILE.write('\n[{0}] [spidy] [ERR]: Please enter a valid integer.'.format(get_time()))
		raise SyntaxError('[{0}] [spidy] [ERR]: Please enter a valid integer.'.format(get_time()))
	else:
		MAX_NEW_MIMES = int(INPUT)

	# Remove INPUT variable from memory
	del INPUT

# Import saved TODO file data
if OVERWRITE:
	write_log('[INIT]: Creating save files...')
	TODO = START
	DONE = []
else:
	write_log('[INIT]: Loading save files...')
	with open(TODO_FILE, 'r') as f:
		contents = f.readlines()
	TODO = [x.strip() for x in contents]
	# Import saved done file data
	with open(DONE_FILE, 'r') as f:
		contents = f.readlines()
	DONE = [x.strip() for x in contents]
	del contents

	# If TODO list is empty, add default starting pages
	if len(TODO) == 0:
		TODO += START


def main():
	# Declare global variables
	global VERSION, START_TIME, START_TIME_LONG
	global LOG_FILE, LOG_FILE_NAME, ERR_LOG_FILE_NAME
	global HEADER, CRAWLER_DIR, KILL_LIST, BAD_LINKS, LOG_END
	global COUNTER, NEW_ERROR_COUNT, KNOWN_ERROR_COUNT, HTTP_ERROR_COUNT, NEW_MIME_COUNT
	global MAX_NEW_ERRORS, MAX_KNOWN_ERRORS, MAX_HTTP_ERRORS, MAX_NEW_MIMES
	global OVERWRITE, RAISE_ERRORS, ZIP_FILES, SAVE_WORDS, SAVE_PAGES, SAVE_COUNT
	global TODO_FILE, DONE_FILE, ERR_LOG_FILE, WORD_FILE, BAD_FILE
	global WORDS, TODO, DONE

	write_log('[INIT]: Successfully started spidy Web Crawler version {0}...'.format(VERSION))
	log('LOG: Successfully started crawler.')

	write_log('[INFO]: TODO first value: {0}'.format(TODO[0]))

	write_log('[INFO]: Using headers: {0}'.format(HEADER))

	while len(TODO) != 0:  # While there are links to check
		try:
			if NEW_ERROR_COUNT >= MAX_NEW_ERRORS or KNOWN_ERROR_COUNT >= MAX_KNOWN_ERRORS or HTTP_ERROR_COUNT >= MAX_HTTP_ERRORS or NEW_MIME_COUNT >= MAX_NEW_MIMES:  # If too many errors have occurred
				write_log('[INFO]: Too many errors have accumulated, stopping crawler.')
				save_files(WORDS)
				sys.exit()
			elif COUNTER >= SAVE_COUNT:  # If it's time for an autosave
				try:
					write_log('[INFO]: Queried {0} links.'.format(str(COUNTER)))
					info_log()
					write_log('[INFO]: Saving files...')
					save_files(WORDS)
					if ZIP_FILES:
						zip_files(t.time(), 'saved/')
				finally:
					# Reset variables
					COUNTER = 0
					WORDS.clear()
					BAD_LINKS.clear()
			elif check_link(TODO[0]):  # If the link is invalid
				del TODO[0]
			# Run
			else:
				page = requests.get(TODO[0], headers=HEADER)  # Get page
				if SAVE_WORDS:
					word_list = make_words(page)  # Get all words from page
					WORDS.update(word_list)  # Add words to word list
				try:
					links = [link for element, attribute, link, pos in html.iterlinks(page.content)]
				except (etree.XMLSyntaxError, etree.ParserError):
					links = []
				links = list(set(links))  # Remove duplicates and shuffle links
				links = [link for link in links if not check_link(link)]
				TODO += links  # Add scraped links to the TODO list
				DONE.append(TODO[0])  # Add crawled link to done list
				if SAVE_PAGES:
					save_page(TODO[0], page)
				if SAVE_WORDS:
					# Announce which link was crawled
					write_log('[CRAWL]: Found {0} links and {1} words on {2}'.format(len(word_list), len(links), TODO[0]))
				else:
					# Announce which link was crawled
					write_log('[CRAWL]: Found {0} links on {1}'.format(len(links), TODO[0]))
				del TODO[0]  # Remove crawled link from TODO list
				COUNTER += 1

		# ERROR HANDLING
		except KeyboardInterrupt:  # If the user does ^C
			handle_keyboard_interrupt()

		except Exception as e:
			link = TODO[0].encode('utf-8', 'ignore')
			write_log('[INFO]: An error was raised trying to process {0}'.format(link))
			err_mro = type(e).mro()

			# HTTP Errors
			if str(e) == 'HTTP Error 403: Forbidden':
				write_log('[ERR]: HTTP 403: Access Forbidden.')
				BAD_LINKS.add(link)

			elif str(e) == 'HTTP Error 429: Too Many Requests':
				write_log('[ERR]: HTTP 429: Too Many Requests.')
				TODO += TODO[0]  # Move link to end of TODO list

			elif etree.XMLSyntaxError in err_mro or etree.ParserError in err_mro:  # Error processing html/xml
				KNOWN_ERROR_COUNT += 1
				write_log('[ERR]: An XMLSyntaxError occurred. A web dev screwed up somewhere.')
				err_log(link, 'XMLSyntaxError', e)

			elif UnicodeError in err_mro:  # Error trying to convert foreign characters to Unicode
				KNOWN_ERROR_COUNT += 1
				write_log('[ERR]: A UnicodeError occurred. URL had a foreign character or something.')
				err_log(link, 'UnicodeError', e)

			elif requests.exceptions.SSLError in err_mro:  # Invalid SSL certificate
				KNOWN_ERROR_COUNT += 1
				write_log('[ERR]: An SSLError occurred. Site is using an invalid certificate.')
				err_log(link, 'SSLError', e)
				BAD_LINKS.add(link)

			elif requests.exceptions.ConnectionError in err_mro:  # Error connecting to page
				KNOWN_ERROR_COUNT += 1
				write_log('[ERR]: A ConnectionError occurred. There\'s something wrong with somebody\'s network.')
				err_log(link, 'ConnectionError', e)

			elif requests.exceptions.TooManyRedirects in err_mro:  # Exceeded 30 redirects.
				KNOWN_ERROR_COUNT += 1
				write_log('[ERR]: A TooManyRedirects error occurred. Page is probably part of a redirect loop.')
				err_log(link, 'TooManyRedirects', e)
				BAD_LINKS.add(link)

			elif requests.exceptions.ContentDecodingError in err_mro:
				# Received response with content-encoding: gzip, but failed to decode it.
				KNOWN_ERROR_COUNT += 1
				write_log('[ERR]: A ContentDecodingError occurred. Probably just a zip bomb, nothing to worry about.')
				err_log(link, 'ContentDecodingError', e)

			elif OSError in err_mro:
				KNOWN_ERROR_COUNT += 1
				write_log('[ERR]: An OSError occurred.')
				err_log(link, 'OSError', e)
				BAD_LINKS.add(link)

			elif 'Unknown MIME type' in str(e):
				NEW_MIME_COUNT += 1
				write_log('[ERR]: Unknown MIME type: {0}'.format(str(e)[18:]))
				err_log(link, 'Unknown MIME', e)

			else:  # Any other error
				NEW_ERROR_COUNT += 1
				write_log('[ERR]: An unknown error happened. New debugging material!')
				err_log(link, 'Unknown', e)
				if RAISE_ERRORS:
					LOG_FILE.close()
					save_files(WORDS)
					raise e
				else:
					continue

			write_log('[LOG]: Saved error message and timestamp to error log file.')
			del TODO[0]
			COUNTER += 1
		finally:
			try:
				TODO = list(set(TODO))  # Removes duplicates and shuffles links so trees don't form.
				# For debugging purposes; to check one link and then stop:
				# save_files(WORDS)
				# sys.exit()
			except KeyboardInterrupt:
				handle_keyboard_interrupt()

	write_log('[INFO]: I think you\'ve managed to download the internet. I guess you\'ll want to save your files...')
	save_files(WORDS)
	LOG_FILE.close()


if __name__ == '__main__':
	main()
else:
	write_log('[INIT]: Successfully imported spidy Web Crawler.')
