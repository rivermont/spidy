'''
Python Web Crawler
Built by rivermont and FalconWarriorr
'''


############
## IMPORT ##
############

#Time statements.
#This is done before anything else to enable timestamp logging at every step.
import time as t
startTime = int(t.time())
def get_time():
	return t.strftime('%H:%M:%S')

print('[{0}] [INIT]: Importing libraries...'.format(get_time()))

#Import required libraries
from lxml import html
from lxml import etree
from os import makedirs
import requests
import sys
import urllib.request
import shutil


###############
## FUNCTIONS ##
###############

print('[{0}] [INIT]: Creating functions...'.format(get_time()))

def check_link(item):
	'''
	Returns True if item is not a valid url.
	Returns False if item passes all inspections (is valid url).
	'''
	if len(item) < 10: #Shortest possible url being 'http://a.b'
		return True
	elif len(item) > 250: #Links longer than 250 characters usually are useless or full of foreign characters
		return True
	elif item[0:4] != 'http': #Must be an http or https link
		return True
	elif item in done: #Can't have visited already
		return True
	else:
		for badLink in killList:
			if badLink in item:
				return True
	return False

def check_word(word):
	'''
	Returns True if word is not valid.
	Returns False if word passes all inspections (is valid).
	'''
	if len(word) > 16: #If word is longer than 16 characters (avg password length is ~8)
		return True
	else:
		return False

def check_extension(path):
	'''
	Returns True if file should be saved as .html.
	Returns False if file extension is (probably) a valid type.
	'''
	if path in ['com', 'com/', 'org', 'org/', 'net', 'net/']:
		return True
	elif len(path) > 5:
		return True
	elif path[-1] == '/':
		return True
	else:
		return False

def make_words(page):
	'''
	Returns list of all valid words in page.
	'''
	page = str(page.content) #Get page content
	wordList = page.split() #Split content into lits of words, as separated by spaces
	wordList = list(set(wordList)) #Remove duplicates
	for word in wordList:
		if check_word(word): #If word is invalid
			wordList.remove(word) #Remove invalid word from list
	return wordList

def save_files(wordList):
	'''
	Saves the TODO and done lists into their respective files.
	Also logs the action to the console.
	'''
	with open(todoFile, 'w') as todoList:
		for site in todo:
			todoList.write(str(site.encode('utf-8'))[2:-1] + '\n') #Save TODO list
		print('[{0}] [LOG]: Saved TODO list to {1}'.format(get_time(), todoFile))
	with open(doneFile, 'w') as doneList:
		for site in done:
			doneList.write(str(site.encode('utf-8'))[2:-1] + '\n') #Save done list
		print('[{0}] [LOG]: Saved done list to {1}'.format(get_time(), doneFile))
	update_file(wordFile, wordList, 'words')
	update_file(badFile, badLinks, 'bad links')

def save_page(url):
	'''
	Download content of page and save to the save folder.
	'''
	url = str(url) #Sanitize input
	newUrl = url
	ext = newUrl.split('.')[-1] #Get all characters from the end of the url to the last period - the file extension, hopefully
	for char in '''"/\ ''': #Replace folders with -
		newUrl = newUrl.replace(char, '-')
	for char in '''|:?<>*''': #Remove illegal filename characters
		newUrl = newUrl.replace(char, '')
	if check_extension(ext): #If the extension is invalid, default to .html
		ext = 'html'
	newUrl = newUrl.replace(ext, '') #Remove extension from file name
	fileName = newUrl + '.' + ext #Create full file name
	with urllib.request.urlopen(url) as response, open('{0}/saved/{1}'.format(crawlerLocation, fileName), 'wb+') as saveFile:
		shutil.copyfileobj(response, saveFile)

def update_file(file, content, type):
	with open(file, 'r+') as f: #Open save file for reading and writing
		fileContent = f.readlines() #Make list of all lines in file
		fileContent = [x.strip() for x in fileContent]
		for item in fileContent:
			content.update(item) #Otherwise add item to content (set)
		for item in content:
			f.write('\n' + item) #Write all words to file
		f.truncate() #Delete everything in file beyond what has been written (old stuff)
	print('[{0}] [LOG]: Saved {1} {2} to {3}'.format(get_time(), len(content), type, file))

def info_log():
	'''
	Logs important information to the console and log file.
	'''
	sinceStart = int(t.time() - startTime)
	invalidLinkPercent = int(sum(invalidLinkPercents) / len(invalidLinkPercents))
	#Print to console
	time = get_time()
	print('[{0}] [LOG]: {1} seconds elapsed since start.'.format(time, sinceStart))
	print('[{0}] [LOG]: {1} links in TODO.'.format(time, len(todo)))
	print('[{0}] [LOG]: {1} links in done.'.format(time, len(done)))
	print('[{0}] [LOG]: {1} bad links removed.'.format(time, removedCount))
	print('[{0}] [LOG]: {1}% of links were bad.'.format(time, invalidLinkPercent))
	print('[{0}] [LOG]: {1} new errors caught.'.format(time, newErrorCount))
	print('[{0}] [LOG]: {1} known errors caught.'.format(time, knownErrorCount))
	#Save to logFile
	fullTime = t.strftime('%H:%M:%S, %A %b %Y') #Get current time
	with open(logFile, 'a') as log:
		log.write('\n\n====AUTOSAVE===') #Write opening line
		log.write('\nTIME: {0}\nSECS ELAPSED: {1}\nTODO: {2}\nDONE: {3}\nREMOVED: {4}\nBAD: {5}%\nNEW ERRORS: {6}\nOLD ERRORS: {7}'.format(time, sinceStart, len(todo), len(done), removedCount, invalidLinkPercent, newErrorCount, knownErrorCount))
		log.write(endLog) #Write closing line

def log(message):
	'''
	Logs a single message.
	Prints message verbatim, so message must formatted correctly outside of the function call.
	'''
	time = t.strftime('%H:%M:%S, %A %b %Y') #Get the current time
	with open(logFile, 'a') as log:
		log.write('\n\n======LOG======') #Write opening line
		log.write('\nTIME: {0}'.format(time)) #Write current time
		log.write(message) #Write message
		log.write(endLog) #Write closing line

def err_print(item):
	'''
	Announce that an error occurred.
	'''
	print('[{0}] [ERR]: An error was raised trying to process {1}'.format(get_time(), item))

def err_saved_message():
	'''
	Announce that error was successfully saved to log.
	'''
	print('[{0}] [LOG]: Saved error message and timestamp to {1}'.format(get_time(), logFile))

def err_log(error1, error2):
	'''
	Saves the triggering error to the log file.
	error1 is the trimmed error source.
	error2 is the extended text of the error.
	'''
	time = t.strftime('%H:%M:%S, %A %b %Y') #Get the current time
	with open(logFile, 'a') as log:
		try:
			log.write('\n\n=====ERROR=====') #Write opening line
			log.write('\nTIME: {0}\nURL: {1}\nERROR: {2}\nEXT: {3}'.format(time, todo[0], error1, str(error2)))
			log.write(endLog) #Write closing line
		except: #If an error (usually UnicodeEncodeError), write encoded log
			log.write('\n\n=====ERROR=====') #Write opening line
			log.write('\nTIME: {0}\nURL: {1}\nERROR: {2}\nEXT: {3}'.format(time, str(todo[0].encode('utf-8')), error1, str(error2)))
		log.write(endLog) #Write closing line

def get_avg(state1, state2):
	'''
	Takes two values and returns the percentage of state1 that is state2.
	'''
	if state1 == 0:
		return 0
	else:
		return (state2 / state1) * 100

def zip(out_fileName, dir):
	'''
	Creates a .zip file in the current directory containing all contents of dir, then deletes dir.
	'''
	shutil.make_archive(str(out_fileName), 'zip', dir) #Zips files
	shutil.rmtree(dir) #Deletes folder
	makedirs(dir[:-1]) #Creates empty folder of same name (minus the '/')
	print('[{0}] [LOG]: Zipped documents to {1}.zip'.format(get_time(), out_filename))


##########
## INIT ##
##########

print('[{0}] [INIT]: Creating variables...'.format(get_time()))

#Initialize required variables

invalidLinkPercents = []

#User-Agent Header String
headers = {
'User-Agent': 'Mozilla/5.0 (compatible; spidy (bot, +https://github.com/rivermont/spidy))'
}

#Folder location of spidy
crawlerLocation = 'C:/Users/Will Bennett/Documents/Code/web-crawler'

#Fallback pages in case the TODO file is empty
start = ['https://en.wikipedia.org/wiki/Main_Page', 'https://www.reddit.com/', 'https://www.google.com/']

#Pages that cause problems with the crawler in some way
killList = ['http://scores.usaultimate.org/', 'https://web.archive.org/web/']

#Empty set for error-causing links
badLinks = set([])

#Empty set for word scraping
words = set([])

#Counter variables
counter = 0
autoSaveCounter = 0
removedCount = 0
newErrorCount = 0
knownErrorCount = 0
HTTPErrorCount = 0

#Amount of errors allowed to happen before automatic shutdown
maxNewErrors = 10
maxKnownErrors = 20
maxHTTPErrors = 50

#Line to print at the end of each logFile log
endLog = '\n======END======'

yes = ['y', 'yes', 'Y', 'Yes']
no = ['n', 'no', 'N', 'No']

#Getting arguments

print('Please enter the following arguments. Leave blank to use the default values.')

overwrite = input('Should spidy load from existing save files? (y/n)')
if not bool(overwrite): #Use default value
	overwrite = False
elif overwrite in yes: #Yes
	overwrite = True
elif overwrite in no: #No
	overwrite = False
else: #Invalid input
	raise InputError('Please enter a valid input. (yes/no)')

raiseErrors = input('Should spidy raise NEW errors and stop crawling? (y/n)')
if not bool(raiseErrors):
	raiseErrors = False
elif raiseErrors in yes:
	raiseErrors = True
elif raiseErrors in no:
	raiseErrors = False
else:
	raise InputError('Please enter a valid input. (yes/no)')

zipFiles = input('Should spidy zip saved documents when autosaving? (y/n)')
if not bool(zipFiles):
	zipFiles = True
elif zipFiles in yes:
	zipFiles = True
elif zipFiles in no:
	zipFiles = False
else:
	raise InputError('Please enter a valid input. (yes/no)')

todoFile = input('Location of the TODO save file:')
if not bool(todoFile):
	todoFile = 'crawler_todo.txt'
else:
	todoFile = todoFile

doneFile = input('Location of the done save file:')
if not bool(doneFile):
	doneFile = 'crawler_done.txt'
else:
	doneFile = doneFile

logFile = input('Location of spidy\'s log file:')
if not bool(logFile):
	logFile = 'crawler_log.txt'
else:
	logFile = logFile

wordFile = input('Location of the word save file:')
if not bool(wordFile):
	wordFile = 'crawler_words.txt'
else:
	wordFile = wordFile

badFile = input('Location of the bad link save file:')
if not bool(badFile):
	badFile = 'crawler_bad.txt'
else:
	badFile = badFile

saveCount = input('After how many queried links should spidy autosave? (default 100)')
if not bool(saveCount):
	saveCount = 100
elif not saveCount.isdigit():
	raise InputError('Please enter a valid integer.')
else:
	saveCount = saveCount

#Import saved TODO file data
if overwrite:
	print('[{0}] [INIT]: Creating save files...'.format(get_time()))
	todo = start
	done = []
else:
	print('[{0}] [INIT]: Loading save files...'.format(get_time()))
	with open(todoFile, 'r') as f:
		todo = f.readlines()
	todo = [x.strip() for x in todo]
	#Import saved done file data
	with open(doneFile, 'r') as f:
		done = f.readlines()
	done = [x.strip() for x in done]

	print('[{0}] [INIT]: Pruning invalid links from TODO...'.format(get_time()))

	before = len(todo)

	#Remove invalid links from TODO list
	for link in todo:
		if check_link(link):
			todo.remove(link)

	#If TODO list is empty, add default start page
	if len(todo) == 0:
		todo += start

	after = before - len(todo)
	removedCount += after
	print('[{0}] [INIT]: {1} invalid links removed from TODO.'.format(get_time(), after))

print('[{0}] [INIT]: TODO first value: {1}'.format(get_time(), todo[0]))

print('[{0}] [INIT]: Starting crawler...'.format(get_time()))
log('\nTIME: {0}\nLOG: Successfully started crawler.'.format(get_time()))


#########
## RUN ##
#########

while len(todo) != 0: #While there are links to check
	try:
		if newErrorCount >= maxNewErrors or knownErrorCount >= maxKnownErrors or HTTPErrorCount >= maxHTTPErrors: #If too many errors have occurred
			print('[{0}] [ERR]: Too many errors have accumulated, stopping crawler.'.format(get_time()))
			save_files(words)
			exit()
		elif counter >= saveCount: #If it's time for an autosave
			print('[{0}] [LOG]: Queried {1} links. Saving files...'.format(get_time(), str(counter)))
			save_files(words)
			info_log()
			if zipFiles:
				zip(t.time(), 'saved/')
			#Reset variables
			counter = 0
			words.clear()
			invalidLinkPercents.clear()
			badLinks.clear()
		elif check_link(todo[0]): #If the link is invalid
			del todo[0]
			continue
		#Run
		else:
			page = requests.get(todo[0], headers=headers) #Get page
			wordList = make_words(page) #Get all words from page
			words.update(wordList) #Add words to word list
			links = []
			for element, attribute, link, pos in html.iterlinks(page.content): #Get all links on the page
				links.append(link)
			before = len(links)
			links = (list(set(links))) #Remove duplicates and shuffle links
			after = len(links)
			invalidLinkPercents.append(get_avg(before, after)) #Get percentage of links removed
			for link in links: #Check for invalid links
				if check_link(link):
					links.remove(link)
					removedCount += 1
				link = link.encode('utf-8') #Encode each link to UTF-8 to minimize errors
			todo += links #Add scraped links to the TODO list
			done.append(todo[0]) #Add crawled link to done list
			save_page(todo[0])
			print('[{0}] [CRAWL]: Found {1} links and {2} words on {3}'.format(get_time(), len(wordList), len(links), todo[0])) #Announce which link was crawled
			del todo[0]#Remove crawled link from TODO list
	
	#ERROR HANDLING
	except KeyboardInterrupt as e: #If the user does ^C
		err_print(todo[0])
		print('[{0}] [ERR]: User performed a KeyboardInterrupt, stopping crawler...'.format(get_time()))
		log('\nLOG: User performed a KeyboardInterrupt, stopping crawler.')
		save_files(words)
		exit()
	except urllib.error.HTTPError as e: #Bad HTTP Response
		HTTPErrorCount += 1
		badLinks.add(todo[0])
		err_print(todo[0])
		print('[{0}] [ERR]: Bad HTTP response.'.format(get_time()))
		err_log('Bad Response', e)
		err_saved_message()
		del todo[0]
	except (etree.XMLSyntaxError, etree.ParserError) as e: #Error processing html/xml
		knownErrorCount += 1
		err_print(todo[0])
		print('[{0}] [ERR]: An XMLSyntaxError occured. A web dev screwed up somewhere.'.format(get_time()))
		err_log('XMLSyntaxError', e)
		err_saved_message()
	except UnicodeError as e: #Error trying to convert foreign characters to Unicode
		knownErrorCount += 1
		err_print(todo[0].encode('utf-8'))
		print('[{0}] [ERR]: A UnicodeError occurred. URL had a foreign character or something.'.format(get_time()))
		err_log('UnicodeError', e)
		err_saved_message()
	except requests.exceptions.SSLError as e: #Invalid SSL certificate
		knownErrorCount += 1
		err_print(todo[0])
		print('[{0}] [ERR]: An SSLError occured. Site is using an invalid certificate.'.format(get_time()))
		err_log('SSLError', e)
		err_saved_message()
	except requests.exceptions.ConnectionError as e: #Error connecting to page
		knownErrorCount += 1
		err_print(todo[0])
		print('[{0}] [ERR]: A ConnectionError occurred. There is something wrong with somebody\'s network.'.format(get_time()))
		err_log('ConnectionError', e)
		err_saved_message()
	except requests.exceptions.TooManyRedirects as e: #Exceeded 30 redirects.
		knownErrorCount += 1
		err_print(todo[0])
		print('[{0}] [ERR]: A TooManyRedirects error occurred. Page is probably part of a redirect loop.'.format(get_time()))
		err_log('TooManyRedirects', e)
		err_saved_message()
	except requests.exceptions.ContentDecodingError as e: #Received response with content-encoding: gzip, but failed to decode it.
		knownErrorCount += 1
		err_print(todo[0])
		print('[{0}] [ERR]: A ContentDecodingError occurred. Probably just a zip bomb, nothing to worry about.'.format(get_time()))
		err_log('ContentDecodingError', e)
		err_saved_message()
	except OSError as e:
		knownErrorCount += 1
		err_print(todo[0])
		print('[{0}] [ERR]: An OSError occurred.'.format(get_time()))
		err_log('OSError', e)
		err_saved_message()
	except Exception as e: #Any other error
		newErrorCount += 1
		err_print(todo[0])
		print('[{0}] [ERR]: An unknown error happened. New debugging material!'.format(get_time()))
		err_log('Unknown', e)
		err_saved_message()
		if raiseErrors:
			raise
		else:
			continue
	finally:
		counter += 1
		#For debugging purposes; to check one link and then stop
		# save_files(words)
		# exit()

print('[{0}] [GOD]: How the hell did this happen? I think you\'ve managed to download the internet. I guess you\'ll want to save your files...'.format(get_time()))
save_files(words)
