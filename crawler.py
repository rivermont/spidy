'''
Python Web Crawler
Built by rivermont and FalconWarriorr
'''

##########
## INIT ##
##########

print('[INIT]: Importing libraries...')

#Import required libraries
from lxml import html
import requests
import sys
import time as t

print('[INIT]: Creating variables...')

#Initialize required variables

start = ['http://www.shodor.org/~wbennett/crawler-home.html', 'https://en.wikipedia.org/wiki/Main_Page', 'https://www.reddit.com/', 'https://www.google.com/']

counter = 0

removedCount = 0

newErrorCount = 0
knownErrorCount = 0

maxNewErrors = 10
maxKnownErrors = 25

print('[INIT]: Reading arguments...')

#Read variables from arguments or set to defaults.

try:
	todoFile = sys.argv[1]
except:
	todoFile = 'crawler_todo.txt'
	pass

try:
	doneFile = sys.argv[2]
except:
	doneFile = 'crawler_done.txt'
	pass

try:
	logFile = sys.argv[3]
except:
	logFile = 'crawler_log.txt'
	pass

try:
	saveCount = int(sys.argv[4])
except:
	saveCount = 100
	#100 is usually around 30 seconds between saves
	pass

print('[INIT]: Loading save files...')

#Import saved TODO file data
with open(todoFile, 'r') as f:
	todo = f.readlines()
todo = [x.strip() for x in todo]

#Import saved done file data
with open(doneFile, 'r') as f:
	done = f.readlines()
done = [x.strip() for x in done]

print('[INIT]: Creating functions...')

def check(item):
	'''
	Checks whether item has been checked, doesn't start with 'h' (must be http, https), or is less than 7 characters long (valid url).
	Returns True if item is not a valid url.
	Returns False if it passes all inspections (is valid url).
	'''
	if item in done:
		return True
	elif len(item) < 7:
		return True
	elif len(item) > 250:
		return True
	elif item[0:4] != 'http':
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
	for site in todo:
		todoList.write(str(site.encode('utf-8'))[2:-1] + '\n')
	print('[LOG]: Saved TODO list to {0}'.format(todoFile))
	for site in done:
		doneList.write(str(site.encode('utf-8'))[2:-1] + '\n')
	print('[LOG]: Saved done list to {0}'.format(doneFile))
	#Close things
	todoList.close()
	doneList.close()

def info_log():
	'''
	Logs important information to the console and log file.
	'''
	#Print to console
	time = t.strftime('%H:%M:%S')
	print('[LOG]: {0}'.format(time))
	print('[LOG]: {0} links in TODO.'.format(len(todo)))
	print('[LOG]: {0} links in done.'.format(len(done)))
	print('[LOG]: {0} bad links removed.'.format(removedCount))
	print('[LOG]: {0} new errors caught.'.format(newErrorCount))
	print('[LOG]: {0} known errors caught.'.format(knownErrorCount))
	#Save to logFile
	fullTime = t.strftime('%H:%M:%S, %A %b %Y')
	log = open(logFile, 'a')
	log.write('\n\n====AUTOSAVE===')
	log.write('\nTIME: {0}\nTODO: {1}\nDONE: {2}\nREMOVED: {3}\nNEW ERRORS: {4}\nOLD ERRORS: {5}'.format(time, len(todo), len(done), removedCount, newErrorCount, knownErrorCount))
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
		log.write('\n\n===ERROR===')
		log.write('\nURL: {0}\nTIME: {1}\nERROR: {2}'.format(todo[0], time, str(error)))
		log.write('\n===END===')
	except: #If an error (usually UnicodeEncodeError), write encoded log
		log.write('\n\n===ERROR===')
		log.write('\nURL: {0}\nTIME: {1}\nERROR: {2}'.format(str(todo[0].encode('utf-8')), time, str(error)))
		log.write('\n===END===')
	log.close() #Save the log file
	todo.remove(todo[0]) #Remove unliked link from todo

def err_print():
	print('[ERR]: An error was raised trying to connect to {0}'.format(todo[0]))

def err_saved_message():
	print('[LOG]: Saved error message and timestamp to {0}'.format(logFile))

print('[INIT]: Pruning invalid links from TODO...')

before = len(todo)

#Remove invalid links from TODO list
for link in todo:
	if check(link):
		todo.remove(link)

#If TODO list is empty, add default start page
if len(todo) == 0:
	todo += start

after = before - len(todo)
print('[INIT]: {0} invalid links removed from TODO.'.format(after))
removedCount += after

print('[INIT]: TODO first value: {0}'.format(todo[0]))

print('[INIT]: Starting crawler...')

#########
## RUN ##
#########

while len(todo) != 0: #While there are links to check
	try:
		if counter >= saveCount:
			print('[LOG]: Queried {0} links. Saving files...'.format(str(counter)))
			files_save()
			info_log()
			counter = 0
		elif newErrorCount >= maxNewErrors or knownErrorCount >= maxKnownErrors:
			print('[ERR]: Too many errors have accumulated, stopping crawler.')
			files_save()
			exit()
		if check(todo[0]):
			todo.remove(todo[0])
			removedCount += 1
		else: #Otherwise it must be valid and new, so
			page = requests.get(todo[0]) #Scrape the link's full content
			links = []
			for element, attribute, link, pos in html.iterlinks(page.content):
				links.append(link)
			before = len(links)
			for link in links:
				if check(link):
					links.remove(link)
					continue
				link = link.encode('utf-8') #Encode each link to UTF-8 to minimize errors
			after = before - len(links)
			removedCount += after
			todo += links #Add scraped links to the TODO list
			done.append(todo[0]) #Add crawled link to done list
			print('[CRAWL]: Found {0} links on {1}'.format(len(links), todo[0])) #Announce which link was crawled
			todo.remove(todo[0]) #Remove crawled link from TODO list
		rand = set(todo)  #Convert TODO to set
		todo = list(rand) #and back to list.
						  #This both removes duplicates and mixes up the list, as sets are unordered collections without duplicates
		counter += 1
	#ERROR HANDLING
	except KeyboardInterrupt as e: #If the user does ^C
		print('[ERR]: User performed a KeyboardInterrupt, stopping crawler...')
		files_save()
		exit()
	except UnicodeEncodeError as e:
		knownErrorCount += 1
		err_print()
		print('[ERR]: A UnicodeEncodeError occurred. URL had a foreign character or something.')
		err_log(e)
		err_saved_message()
	except requests.exceptions.SSLError as e:
		knownErrorCount += 1
		err_print()
		print('[ERR]: An SSLError occured. Site is using an invalid certificate.')
		err_log(e)
		err_saved_message()
	except requests.exceptions.TooManyRedirects as e:
		knownErrorCount += 1
		err_print()
		print('[ERR]: A TooManyRedirects error occurred. Page is probably part of a redirect loop.')
		err_log(e)
		err_saved_message()
	except requests.exceptions.ConnectionError as e:
		knownErrorCount += 1
		err_print()
		print('[ERR]: A ConnectionError occurred. There is something wrong with somebody\'s network.')
		err_log(e)
		err_saved_message()
	except requests.exceptions.ContentDecodingError as e:
		knownErrorCount += 1
		err_print()
		print('[ERR]: A ContentDecodingError occurred. Probably just a zip bomb, nothing to worry about.')
		err_log(e)
		err_saved_message()
	except Exception as e: #If any other error is raised
		newErrorCount += 1
		err_print()
		print('[ERR]: An unkown error happened. New debugging material!')
		err_log(e)
		err_saved_message()
		raise
		# continue #Keep going like nothing happened
	# finally: #For debugging purposes, to check one link and then stop
		# files_save()
		# exit()

print('[GOD]: How the hell did this happen? I think you\'ve managed to download the internet. I guess you\'ll want to save your files...')
files_save()
