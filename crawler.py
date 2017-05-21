'''
Python Web Crawler
Built by rivermont and FalconWarriorr
'''

##########
## INIT ##
##########

import time as t
def get_time():
	return t.strftime('%H:%M:%S')

print('[{0}] [INIT]: Importing libraries...'.format(get_time()))

#Import required libraries
from lxml import html
from lxml import etree
import requests
import sys

print('[{0}] [INIT]: Creating variables...'.format(get_time()))

#Initialize required variables

start = ['http://www.shodor.org/~wbennett/crawler-home.html', 'https://en.wikipedia.org/wiki/Main_Page', 'https://www.reddit.com/', 'https://www.google.com/']

counter = 0

removedCount = 0
newErrorCount = 0
knownErrorCount = 0

maxNewErrors = 10
maxKnownErrors = 25

startTime = round(t.time(), 3)

print('[{0}] [INIT]: Reading arguments...'.format(get_time()))

#Read variables from arguments or set to defaults.

try:
	overwrite = sys.argv[1]
except:
	overwrite = False
	pass

try:
	todoFile = sys.argv[2]
except:
	todoFile = 'crawler_todo.txt'
	pass

try:
	doneFile = sys.argv[3]
except:
	doneFile = 'crawler_done.txt'
	pass

try:
	logFile = sys.argv[4]
except:
	logFile = 'crawler_log.txt'
	pass

try:
	saveCount = int(sys.argv[5])
except:
	saveCount = 100
	#100 is usually around 30 seconds between saves
	pass

print('[{0}] [INIT]: Loading save files...'.format(get_time()))

#Import saved TODO file data
with open(todoFile, 'r') as f:
	todo = f.readlines()
todo = [x.strip() for x in todo]

#Import saved done file data
with open(doneFile, 'r') as f:
	done = f.readlines()
done = [x.strip() for x in done]

print('[{0}] [INIT]: Creating functions...'.format(get_time()))

def check(item):
	'''
	Checks whether item has been checked, doesn't start with 'h' (must be http, https), or is less than 7 characters long (valid url).
	Returns True if item is not a valid url.
	Returns False if it passes all inspections (is valid url).
	'''
	if len(item) < 7:
		return True
	elif item[0:4] != 'http':
		return True
	elif item in done:
		return True
	elif len(item) > 250:
		return True
	else:
		return False

def files_save():
	'''
	Saves the TODO and done lists into their respective files.
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
	#Print to console
	time = get_time()
	sinceStart = round(t.time() - startTime, 3)
	print('[{0}] [LOG]: {1} seconds elapsed since start.'.format(time, sinceStart))
	print('[{0}] [LOG]: {1} links in TODO.'.format(time, len(todo)))
	print('[{0}] [LOG]: {1} links in done.'.format(time, len(done)))
	print('[{0}] [LOG]: {1} bad links removed.'.format(time, removedCount))
	print('[{0}] [LOG]: {1} new errors caught.'.format(time, newErrorCount))
	print('[{0}] [LOG]: {1} known errors caught.'.format(time, knownErrorCount))
	#Save to logFile
	fullTime = t.strftime('%H:%M:%S, %A %b %Y')
	log = open(logFile, 'a')
	log.write('\n\n====AUTOSAVE===')
	log.write('\nTIME: {0}\nSECS ELAPSED: {1}\nTODO: {2}\nDONE: {3}\nREMOVED: {4}\nNEW ERRORS: {5}\nOLD ERRORS: {6}'.format(time, sinceStart, len(todo), len(done), removedCount, newErrorCount, knownErrorCount))
	log.write('\n======END======')
	pass

def err_log(error):
	'''
	Saves the triggering error to the log file.
	Format:
	SITE: todo[0]
	TIMER: Hr:Min:Sec, Weekday Month Year
	ERROR: error
	'''
	log = open(logFile, 'a') #Open the log file
	time = t.strftime('%H:%M:%S, %A %b %Y') #Get the current time
	try:
		log.write('\n\n=====ERROR=====')
		log.write('\nTIME: {0}\nURL: {1}\nERROR: {2}'.format(time, todo[0], str(error)))
		log.write('\n======END======')
	except: #If an error (usually UnicodeEncodeError), write encoded log
		log.write('\n\n=====ERROR=====')
		log.write('\nTIME: {0}\nURL: {1}\nERROR: {2}'.format(time, str(todo[0].encode('utf-8')), str(error)))
		log.write('\n======END======')
	log.close() #Save the log file
	todo.remove(todo[0]) #Remove unliked link from todo

def err_print(item):
	print('[{0}] [ERR]: An error was raised trying to connect to {1}'.format(get_time(), item))

def err_saved_message():
	print('[{0}] [LOG]: Saved error message and timestamp to {1}'.format(get_time(), logFile))

print('[{0}] [INIT]: Pruning invalid links from TODO...'.format(get_time()))

before = len(todo)

#Remove invalid links from TODO list
for link in todo:
	if check(link):
		todo.remove(link)

#If TODO list is empty, add default start page
if len(todo) == 0:
	todo += start

after = before - len(todo)
removedCount += after

print('[{0}] [INIT]: {1} invalid links removed from TODO.'.format(get_time(), after))


print('[{0}] [INIT]: TODO first value: {1}'.format(get_time(), todo[0]))

print('[{0}] [INIT]: Starting crawler...'.format(get_time()))

#########
## RUN ##
#########

while len(todo) != 0: #While there are links to check
	try:
		if counter >= saveCount: #If it's not time for an autosave
			print('[{0}] [LOG]: Queried {1} links. Saving files...'.format(get_time(), str(counter)))
			files_save()
			info_log()
			counter = 0
		elif newErrorCount >= maxNewErrors or knownErrorCount >= maxKnownErrors: #If too many errors haven't occurred
			print('[{0}] [ERR]: Too many errors have accumulated, stopping crawler.'.format(get_time()))
			files_save()
			exit()
		if check(todo[0]): #If the link is valid
			todo.remove(todo[0])
			removedCount += 1
		else: #Otherwise it must be valid and new, so
			page = requests.get(todo[0]) #Get page
			links = []
			for element, attribute, link, pos in html.iterlinks(page.content): #Get all links on the page
				links.append(link)
			links = (list(set(links))
			for link in links: #Check for invalid links
				if check(link):
					links.remove(link)
					removedCount += 1
					continue
				link = link.encode('utf-8') #Encode each link to UTF-8 to minimize errors
			todo += links #Add scraped links to the TODO list
			done.append(todo[0]) #Add crawled link to done list
			print('[{0}] [CRAWL]: Found {1} links on {2}'.format(get_time(), len(links), todo[0])) #Announce which link was crawled
			todo.remove(todo[0]) #Remove crawled link from TODO list
		rand = set(todo)  #Convert TODO to set
		todo = list(rand) #and back to list.
						  #This both removes duplicates and mixes up the list, as sets are unordered collections without duplicates
		counter += 1
	#ERROR HANDLING
	except KeyboardInterrupt as e: #If the user does ^C
		print('[{0}] [ERR]: User performed a KeyboardInterrupt, stopping crawler...'.format(get_time()))
		files_save()
		exit()
	except UnicodeEncodeError as e:
		knownErrorCount += 1
		err_print(todo[0].encode('utf-8'))
		print('[{0}] [ERR]: A UnicodeEncodeError occurred. URL had a foreign character or something.'.format(get_time()))
		err_log(e)
		err_saved_message()
	except requests.exceptions.SSLError as e:
		knownErrorCount += 1
		err_print(todo[0])
		print('[{0}] [ERR]: An SSLError occured. Site is using an invalid certificate.'.format(get_time()))
		err_log(e)
		err_saved_message()
	except (etree.XMLSyntaxError, etree.ParserError) as e:
		knownErrorCount += 1
		err_print(todo[0])
		print('[{0}] [ERR]: An XMLSyntaxError occured. A web dev screwed up somewhere.'.format(get_time()))
		err_log(e)
		err_saved_message()
	except requests.exceptions.TooManyRedirects as e:
		knownErrorCount += 1
		err_print(todo[0])
		print('[{0}] [ERR]: A TooManyRedirects error occurred. Page is probably part of a redirect loop.'.format(get_time()))
		err_log(e)
		err_saved_message()
	except requests.exceptions.ConnectionError as e:
		knownErrorCount += 1
		err_print(todo[0])
		print('[{0}] [ERR]: A ConnectionError occurred. There is something wrong with somebody\'s network.'.format(get_time()))
		err_log(e)
		err_saved_message()
	except requests.exceptions.ContentDecodingError as e:
		knownErrorCount += 1
		err_print(todo[0])
		print('[{0}] [ERR]: A ContentDecodingError occurred. Probably just a zip bomb, nothing to worry about.'.format(get_time()))
		err_log(e)
		err_saved_message()
	except Exception as e: #If any other error is raised
		newErrorCount += 1
		err_print(todo[0])
		print('[{0}] [ERR]: An unkown error happened. New debugging material!'.format(get_time()))
		err_log(e)
		err_saved_message()
		raise
		# continue
	# finally: #For debugging purposes; to check one link and then stop
		# files_save()
		# exit()

print('[{0}] [GOD]: How the hell did this happen? I think you\'ve managed to download the internet. I guess you\'ll want to save your files...'.format(get_time()))
files_save()
