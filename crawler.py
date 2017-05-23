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
import requests
import sys


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
	elif item[0:4] != 'http': #Must be an http or https link
		return True
	elif item in done: #Can't have visited already
		return True
	elif len(item) > 250: #Links longer than 250 characters usually are useless or full of foreign characters
		return True
	else:
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

def words_save(wordList):
	with open(wordFile, 'r+') as f: #Open save file for reading and writing
		file = f.readlines() #Make list of all lines in wordFile
		for item in file:
			if check_word(item): #If item is invalid
				file.remove(item) #Remove invalid word from
			elif not check_word(item):
				wordList.update(item) #Otherwise add item to wordList (set)
		for word in wordList:
			f.write('\n' + word) #Write all words to wordFile
		f.truncate() #Delete everything in wordFile beyond what has been written (old stuff)
	print('[{0}] [LOG]: Saved words list to {1}'.format(get_time(), wordFile))

def files_save():
	'''
	Saves the TODO and done lists into their respective files.
	Also logs the action to the console.
	'''
	#Open save files
	todoList = open(todoFile, 'w')
	doneList = open(doneFile, 'w')
	#Save
	time = get_time()
	for site in todo:
		todoList.write(str(site.encode('utf-8'))[2:-1] + '\n')
	print('[{0}] [LOG]: Saved TODO list to {1}'.format(time, todoFile))
	for site in done:
		doneList.write(str(site.encode('utf-8'))[2:-1] + '\n')
	print('[{0}] [LOG]: Saved done list to {1}'.format(time, doneFile))
	#Close things
	todoList.close()
	doneList.close()

def info_log():
	'''
	Logs important information to the console and log file.
	'''
	sinceStart = int(t.time() - startTime)
	badLinkPercent = int(sum(badLinkPercents) / len(badLinkPercents))
	#Print to console
	time = get_time()
	print('[{0}] [LOG]: {1} seconds elapsed since start.'.format(time, sinceStart))
	print('[{0}] [LOG]: {1} links in TODO.'.format(time, len(todo)))
	print('[{0}] [LOG]: {1} links in done.'.format(time, len(done)))
	print('[{0}] [LOG]: {1} bad links removed.'.format(time, removedCount))
	print('[{0}] [LOG]: {1}% of links were bad.'.format(time, badLinkPercent))
	print('[{0}] [LOG]: {1} new errors caught.'.format(time, newErrorCount))
	print('[{0}] [LOG]: {1} known errors caught.'.format(time, knownErrorCount))
	#Save to logFile
	fullTime = t.strftime('%H:%M:%S, %A %b %Y')
	log = open(logFile, 'a')
	log.write('\n\n====AUTOSAVE===')
	log.write('\nTIME: {0}\nSECS ELAPSED: {1}\nTODO: {2}\nDONE: {3}\nREMOVED: {4}\nBAD: {5}%\nNEW ERRORS: {6}\nOLD ERRORS: {7}'.format(time, sinceStart, len(todo), len(done), removedCount, badLinkPercent, newErrorCount, knownErrorCount))
	log.write(endLog)

def err_log(error1, error2):
	'''
	Saves the triggering error to the log file.
	error1 is the trimmed error source.
	error2 is the extended text of the error.
	'''
	log = open(logFile, 'a') #Open the log file
	time = t.strftime('%H:%M:%S, %A %b %Y') #Get the current time
	try:
		log.write('\n\n=====ERROR=====')
		log.write('\nTIME: {0}\nURL: {1}\nERROR: {2}\nEXT: {3}'.format(time, todo[0], error1, str(error2)))
		log.write(endLog)
	except: #If an error (usually UnicodeEncodeError), write encoded log
		log.write('\n\n=====ERROR=====')
		log.write('\nTIME: {0}\nURL: {1}\nERROR: {2}\nEXT: {3}'.format(time, str(todo[0].encode('utf-8')), error1, str(error2)))
		log.write(endLog)
	log.close() #Save the log file

def log(message):
	'''
	Logs a single message.
	Prints message verbatim, so message must formatted correctly outside of the function call.
	'''
	log = open(logFile, 'a') #Open the log file
	time = t.strftime('%H:%M:%S, %A %b %Y') #Get the current time
	log.write('\n\n======LOG======')
	log.write(message)
	log.write(endLog)
	log.close()

def err_print(item):
	print('[{0}] [ERR]: An error was raised trying to connect to {1}'.format(get_time(), item))

def err_saved_message():
	print('[{0}] [LOG]: Saved error message and timestamp to {1}'.format(get_time(), logFile))

def get_avg(state1, state2):
	'''
	Takes two values and returns the percentage of state1 that is state2.
	'''
	if state1 == 0:
		return 0
	else:
		return (state2 / state1) * 100


##########
## INIT ##
##########

print('[{0}] [INIT]: Creating variables...'.format(get_time()))

#Initialize required variables

#Fallback pages in case the TODO file is empty
start = ['http://www.shodor.org/~wbennett/crawler-home.html', 'https://en.wikipedia.org/wiki/Main_Page', 'https://www.reddit.com/', 'https://www.google.com/']

#Counter variables
counter = 0
removedCount = 0
newErrorCount = 0
knownErrorCount = 0

badLinkPercents = []

words = set([])

#Amount of errors allowed to happen before automatic shutdown
maxNewErrors = 10
maxKnownErrors = 25

#Line to print at the end of each logFile log
endLog = '\n======END======'

print('[{0}] [INIT]: Reading arguments...'.format(get_time()))

#Read variables from arguments or set to defaults if args not present.

try: #Whether to load from save files or overwrite them
	overwrite = sys.argv[1]
except:
	overwrite = False
	pass

try: #Whether to raise errors instead of passing them
	raiseErrors = sys.argv[2]
except:
	raiseErrors = False
	pass

try: #Saved TODO file location
	todoFile = sys.argv[3]
except:
	todoFile = 'crawler_todo.txt'
	pass

try: #Saved done file location
	doneFile = sys.argv[4]
except:
	doneFile = 'crawler_done.txt'
	pass

try: #Saved log file location
	logFile = sys.argv[5]
except:
	logFile = 'crawler_log.txt'
	pass

try: #Saved words file location
	wordFile = sys.argv[6]
except:
	wordFile = 'crawler_words.txt'

try: #Number of crawled links after which to autosave
	saveCount = int(sys.argv[7])
except:
	saveCount = 100
	#100 is default as it means there is usually at least one log in the console window at any given time.
	pass

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
		if counter >= saveCount: #If it's not time for an autosave
			print('[{0}] [LOG]: Queried {1} links. Saving files...'.format(get_time(), str(counter)))
			files_save()
			words_save(words)
			words.clear()
			info_log()
			counter = 0
		elif newErrorCount >= maxNewErrors or knownErrorCount >= maxKnownErrors: #If too many errors haven't occurred
			print('[{0}] [ERR]: Too many errors have accumulated, stopping crawler.'.format(get_time()))
			files_save()
			exit()
		elif check_link(todo[0]):
			continue
		else:
			page = requests.get(todo[0]) #Get page
			words.update(make_words(page))
			links = []
			for element, attribute, link, pos in html.iterlinks(page.content): #Get all links on the page
				links.append(link)
			before = len(links)
			links = (list(set(links)))
			after = len(links)
			badLinkPercents.append(get_avg(before, after))
			for link in links: #Check for invalid links
				if check_link(link):
					links.remove(link)
					removedCount += 1
					continue
				link = link.encode('utf-8') #Encode each link to UTF-8 to minimize errors
			todo += links #Add scraped links to the TODO list
			done.append(todo[0]) #Add crawled link to done list
			print('[{0}] [CRAWL]: Found {1} links on {2}'.format(get_time(), len(links), todo[0])) #Announce which link was crawled
	
	#ERROR HANDLING
	except KeyboardInterrupt as e: #If the user does ^C
		err_print(todo[0])
		print('[{0}] [ERR]: User performed a KeyboardInterrupt, stopping crawler...'.format(get_time()))
		log('\nTIME: {0}\nLOG: User performed a KeyboardInterrupt, stopping crawler.'.format(get_time()))
		files_save()
		exit()
	except requests.exceptions.ConnectionError as e: # HTTP(S)ConnectionPool: Max retries exceeded with url
		knownErrorCount += 1
		err_print(todo[0])
		print('[{0}] [ERR]: A ConnectionError occurred. There is something wrong with somebody\'s network.'.format(get_time()))
		err_log('ConnectionError', e)
		err_saved_message()
	except UnicodeEncodeError as e: # 'charmap' codec can't encode characters
		knownErrorCount += 1
		err_print(todo[0].encode('utf-8'))
		print('[{0}] [ERR]: A UnicodeEncodeError occurred. URL had a foreign character or something.'.format(get_time()))
		err_log('UnicodeEncodeError', e)
		err_saved_message()
	except requests.exceptions.SSLError as e: # SSL: CERTIFICATE_VERIFY_FAILED
		knownErrorCount += 1
		err_print(todo[0])
		print('[{0}] [ERR]: An SSLError occured. Site is using an invalid certificate.'.format(get_time()))
		err_log('SSLError', e)
		err_saved_message()
	except (etree.XMLSyntaxError, etree.ParserError) as e:
		knownErrorCount += 1
		err_print(todo[0])
		print('[{0}] [ERR]: An XMLSyntaxError occured. A web dev screwed up somewhere.'.format(get_time()))
		err_log('XMLSyntaxError', e)
		err_saved_message()
	except requests.exceptions.TooManyRedirects as e: # Exceeded 30 redirects.
		knownErrorCount += 1
		err_print(todo[0])
		print('[{0}] [ERR]: A TooManyRedirects error occurred. Page is probably part of a redirect loop.'.format(get_time()))
		err_log('TooManyRedirects', e)
		err_saved_message()
	except requests.exceptions.ContentDecodingError as e: # Received response with content-encoding: gzip, but failed to decode it.
		knownErrorCount += 1
		err_print(todo[0])
		print('[{0}] [ERR]: A ContentDecodingError occurred. Probably just a zip bomb, nothing to worry about.'.format(get_time()))
		err_log('ContentDecodingError', e)
		err_saved_message()
	except OSError as e:
		knownErrorCount += 1
		err_print(todo[0])
		print('[{0}] [ERR]: An OSError occurred.')
		err_log('OSError', e)
		err_saved_message()
	except Exception as e: #If any other error is raised
		newErrorCount += 1
		err_print(todo[0])
		print('[{0}] [ERR]: An unkown error happened. New debugging material!'.format(get_time()))
		err_log('Unkown', e)
		err_saved_message()
		if raiseErrors:
			raise
		else:
			continue
	finally:
		counter += 1
		rand = set(todo)  #Convert TODO to set
		todo = list(rand) #and back to list.
						  #This both removes duplicates and mixes up the list, as sets are unordered collections without duplicates
		del todo[0]#Remove crawled link from TODO list
		
		#For debugging purposes; to check one link and then stop
		# files_save()
		# exit()

print('[{0}] [GOD]: How the hell did this happen? I think you\'ve managed to download the internet. I guess you\'ll want to save your files...'.format(get_time()))
files_save()
