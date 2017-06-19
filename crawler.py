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

print('[{0}] [spidy] [INIT]: Importing libraries...'.format(get_time()))

#Import required libraries
import requests
import sys
import urllib.request
import shutil
from lxml import html, etree
from os import makedirs, path


###############
## FUNCTIONS ##
###############

print('[{0}] [spidy] [INIT]: Creating functions...'.format(get_time()))

def get_full_time():
	return t.strftime('%H:%M:%S, %A %b %Y')

def check_link(item):
	'''
	Returns True if item is not a valid url.
	Returns False if item passes all inspections (is valid url).
	'''
	#Shortest possible url being 'http://a.b'
	if len(item) < 10:
		return True
	#Links longer than 255 characters usually are useless or full of foreign characters, and will also cause problems when saving
	elif len(item) > 255:
		return True
	#Must be an http or https link
	elif item[0:4] != 'http':
		return True
	#Can't have visited already
	elif item in done:
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
	#If word is longer than 16 characters (avg password length is ~8)
	if len(word) > 16:
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

def check_path(filePath):
	'''
	Checks the path of a given filename to see whether it will cause errors when saving.
	Returns True if path is valid.
	Returns False if path is invalid.
	'''
	if len(filePath) > 256:
		return False
	else:
		return True

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
	Saves the TODO, done, word, and bad lists into their respective files.
	Also logs the action to the console.
	'''
	with open(todoFile, 'w') as todoList:
		for site in todo:
			try:
				todoList.write(site + '\n') #Save TODO list
			except UnicodeError:
				continue
	print('[{0}] [spidy] [LOG]: Saved TODO list to {1}'.format(get_time(), todoFile))
	
	with open(doneFile, 'w') as doneList:
		for site in done:
			try:
				doneList.write(site + '\n') #Save done list
			except UnicodeErorr:
				continue
	print('[{0}] [spidy] [LOG]: Saved done list to {1}'.format(get_time(), doneFile))
	
	update_file(wordFile, wordList, 'words')
	update_file(badFile, badLinks, 'bad links')

def save_page(url):
	'''
	Download content of page and save to the save folder.
	'''
	url = str(url) #Sanitize input
	newUrl = url
	if newUrl[-1] == '.':
		ext = 'html'
	else:
		ext = newUrl.split('.')[-1] #Get all characters from the end of the url to the last period - the file extension.
	for char in '''"/\ ''': #Replace folders with -
		newUrl = newUrl.replace(char, '-')
	for char in '''|:?<>*''': #Remove illegal filename characters
		newUrl = newUrl.replace(char, '')
	if check_extension(ext): #If the extension is invalid, default to .html
		ext = 'html'
	newUrl = newUrl.replace(ext, '') #Remove extension from file name
	fileName = newUrl + '.' + ext #Create full file name
	path = '{0}/saved/{1}'.format(crawlerLocation, fileName)
	if check_path(path):
		with urllib.request.urlopen(url) as response, open(path, 'wb+') as saveFile:
			shutil.copyfileobj(response, saveFile)
	else:
		log('\nLINK: {0}\nLOG: Filename too long.'.format(url))
		print('[{0}] [spidy] [ERR]: Filename too long, page will not be saved.'.format(get_time()))

def update_file(file, content, type):
	with open(file, 'r+') as f: #Open save file for reading and writing
		fileContent = f.readlines() #Make list of all lines in file
		fileContent = [x.strip() for x in fileContent]
		for item in fileContent:
			content.update(item) #Otherwise add item to content (set)
		for item in content:
			f.write('\n' + str(item)) #Write all words to file
		f.truncate() #Delete everything in file beyond what has been written (old stuff)
	print('[{0}] [spidy] [LOG]: Saved {1} {2} to {3}'.format(get_time(), len(content), type, file))

def info_log():
	'''
	Logs important information to the console and log file.
	'''
	sinceStart = int(t.time() - startTime)
	
	#Print to console
	time = get_time()
	print('[{0}] [spidy] [LOG]: {1} seconds elapsed since start.'.format(time, sinceStart))
	print('[{0}] [spidy] [LOG]: {1} links in TODO.'.format(time, len(todo)))
	print('[{0}] [spidy] [LOG]: {1} links in done.'.format(time, len(done)))
	print('[{0}] [spidy] [LOG]: {1} bad links removed.'.format(time, removedCount))
	print('[{0}] [spidy] [LOG]: {1} new errors caught.'.format(time, newErrorCount))
	print('[{0}] [spidy] [LOG]: {1} HTTP errors encountered.'.format(time, HTTPErrorCount))
	print('[{0}] [spidy] [LOG]: {1} known errors caught.'.format(time, knownErrorCount))
	
	#Save to logFile
	with open(logFile, 'a') as log:
		log.write('\n\n====AUTOSAVE===') #Write opening line
		log.write('\nTIME: {0}\nSECS ELAPSED: {1}\nTODO: {2}\nDONE: {3}\nREMOVED: {4}\nNEW ERRORS: {5}\nHTTP ERRORS: {6}\nOLD ERRORS: {7}'.format(get_full_time(), sinceStart, len(todo), len(done), removedCount, newErrorCount, HTTPErrorCount, knownErrorCount))
		log.write(endLog) #Write closing line

def log(message):
	'''
	Logs a single message to the logFile.
	Prints message verbatim, so message must be formatted correctly outside of the function call.
	'''
	with open(logFile, 'a') as log:
		log.write('\n\n======LOG======') #Write opening line
		log.write('\nTIME: {0}'.format(get_full_time())) #Write current time
		log.write(message) #Write message
		log.write(endLog) #Write closing line

def err_print(item):
	'''
	Announce that an error occurred.
	'''
	print('[{0}] [spidy] [ERR]: An error was raised trying to process {1}'.format(get_time(), item))

def err_saved_message():
	'''
	Announce that error was successfully saved to log.
	'''
	print('[{0}] [spidy] [LOG]: Saved error message and timestamp to {1}'.format(get_time(), logFile))

def err_log(url, error1, error2):
	'''
	Saves the triggering error to the log file.
	error1 is the trimmed error source.
	error2 is the extended text of the error.
	'''
	time = t.strftime('%H:%M:%S, %A %b %Y') #Get the current time
	with open(logFile, 'a') as log:
		log.write('\n\n=====ERROR=====') #Write opening line
		log.write('\nTIME: {0}\nURL: {1}\nERROR: {2}\nTYPE: {3}\nEXT: {4}'.format(time, url, error1, str(error2)[8:-2], str(error2)))
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
	print('[{0}] [spidy] [LOG]: Zipped documents to {1}.zip'.format(get_time(), out_fileName))

##########
## INIT ##
##########

print('[{0}] [spidy] [INIT]: Creating variables...'.format(get_time()))

#Initialize required variables

#User-Agent Header String
headers = {
'User-Agent': 'Mozilla/5.0 (compatible; spidy (bot, +https://github.com/rivermont/spidy))'
}

#Folder location of spidy
crawlerLocation = path.dirname(path.realpath(__file__))

#Web directories to use in case TODO file is empty
directories = [
'https://en.wikipedia.org/wiki/List_of_most_popular_websites',
'http://www.clambr.com/49-free-web-directories-for-building-backlinks/'
# 'https://botw.org/',
# 'http://greenstalk.com/',
# 'http://www.directoryworld.net/',
# 'https://www.somuch.com/',
# 'http://www.jayde.com/',
# 'http://dmoz.in.net/',
# 'http://www.tsection.com/',
# 'http://www.rakcha.com/',
# 'http://www.joeant.com/',
# 'http://www.splashdirectory.com/',
# 'http://www.goguides.org/',
# 'http://www.dataspear.com/',
# 'http://www.zorg-directory.com/',
# 'http://www.gimpsy.com/',
# 'http://www.links2go.com/',
# 'http://www.global-weblinks.com/',
# 'http://www.skaffe.com/',
# 'http://www.nextsbd.com/',
# 'http://www.octopedia.com/',
# 'http://www.info-listings.com/',
# 'https://www.enquira.com/',
# 'http://www.worldsiteindex.com/',
# 'https://www.findwebsite.net/',
# 'http://www.dir4uk.com/',
# 'http://www.royallinkup.com/',
# 'http://www.leadinglinkdirectory.com/',
# 'http://www.visionwebseo.com/',
# 'http://uklistingz.co.uk/',
# 'http://www.webappsdirectory.com/',
# 'http://xysyst.net/',
# 'http://www.10directory.com/%E2%80%9C%20rel=',
# 'http://www.sighbercafe.com/',
# 'http://www.nipao.org/',
# 'https://www.bestfreewebsites.net/',
# 'http://www.linkdir.info/',
# 'http://www.the-net-directory.com/',
# 'http://www.nexusdirectory.com/',
# www.247webdirectory.com
# 'https://www.9sites.net/',
# www.piseries.com
# www.cipinet.com
# 'http://www.synergy-directory.com/',
# 'http://www.wikidweb.com/',
# www.directoryfire.com
# www.prolinkdirectory.com
# www.amray.com
# www.gainweb.org
# www.the-web-directory.co.uk
# 'http://www.submission4u.com/',
# 'http://www.elitesitesdirectory.com/',
# 'http://www.linkpedia.net/',
# 'http://www.scrabblestop.com/dir/',
# 'http://www.inteligentd.com/,',
# 'http://www.pr3plus.com/',
# 'http://www.suggest-url.net/'
]

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

print('[{0}] [spidy] [INIT]: Please enter the following arguments. Leave blank to use the default values.'.format(get_time()))

overwrite = input('[{0}] [spidy] [INPUT]: Should spidy load from existing save files? (y/n)'.format(get_time()))
if not bool(overwrite): #Use default value
	overwrite = False
elif overwrite in yes: #Yes
	overwrite = True
elif overwrite in no: #No
	overwrite = False
else: #Invalid input
	raise SyntaxError('[{0}] [spidy] [ERR]: Please enter a valid input. (yes/no)'.format(get_time()))

raiseErrors = input('[{0}] [spidy] [INPUT]: Should spidy raise NEW errors and stop crawling? (y/n)'.format(get_time()))
if not bool(raiseErrors):
	raiseErrors = False
elif raiseErrors in yes:
	raiseErrors = True
elif raiseErrors in no:
	raiseErrors = False
else:
	raise SyntaxError('[{0}] [spidy] [ERR]: Please enter a valid input. (yes/no)'.format(get_time()))

zipFiles = input('[{0}] [spidy] [INPUT]: Should spidy zip saved documents when autosaving? (y/n)'.format(get_time()))
if not bool(zipFiles):
	zipFiles = True
elif zipFiles in yes:
	zipFiles = True
elif zipFiles in no:
	zipFiles = False
else:
	raise SyntaxError('[{0}] [spidy] [ERR]: Please enter a valid input. (yes/no)'.format(get_time()))

todoFile = input('[{0}] [spidy] [INPUT]: Location of the TODO save file:'.format(get_time()))
if not bool(todoFile):
	todoFile = 'crawler_todo.txt'
else:
	todoFile = todoFile

doneFile = input('[{0}] [spidy] [INPUT]: Location of the done save file:'.format(get_time()))
if not bool(doneFile):
	doneFile = 'crawler_done.txt'
else:
	doneFile = doneFile

logFile = input('[{0}] [spidy] [INPUT]: Location of spidy\'s log file:'.format(get_time()))
if not bool(logFile):
	logFile = 'crawler_log.txt'
else:
	logFile = logFile

wordFile = input('[{0}] [spidy] [INPUT]: Location of the word save file:'.format(get_time()))
if not bool(wordFile):
	wordFile = 'crawler_words.txt'
else:
	wordFile = wordFile

badFile = input('[{0}] [spidy] [INPUT]: Location of the bad link save file:'.format(get_time()))
if not bool(badFile):
	badFile = 'crawler_bad.txt'
else:
	badFile = badFile

saveCount = input('[{0}] [spidy] [INPUT]: After how many queried links should spidy autosave? (default 100)'.format(get_time()))
if not bool(saveCount):
	saveCount = 100
elif not saveCount.isdigit():
	raise SyntaxError('[{0}] [spidy] [ERR]: Please enter a valid integer.'.format(get_time()))
else:
	saveCount = saveCount

#Import saved TODO file data
if overwrite:
	print('[{0}] [spidy] [INIT]: Creating save files...'.format(get_time()))
	todo = directories
	done = []
else:
	print('[{0}] [spidy] [INIT]: Loading save files...'.format(get_time()))
	with open(todoFile, 'r') as f:
		todo = f.readlines()
	todo = [x.strip() for x in todo]
	#Import saved done file data
	with open(doneFile, 'r') as f:
		done = f.readlines()
	done = [x.strip() for x in done]

	print('[{0}] [spidy] [INIT]: Pruning invalid links from TODO...'.format(get_time()))

	before = len(todo)

	#Remove invalid links from TODO list
	for link in todo:
		if check_link(link):
			todo.remove(link)

	#If TODO list is empty, add default starting pages
	if len(todo) == 0:
		todo += directories

	after = abs(before - len(todo))
	removedCount += after
	print('[{0}] [spidy] [INIT]: {1} invalid links removed from TODO.'.format(get_time(), after))

print('[{0}] [spidy] [INIT]: TODO first value: {1}'.format(get_time(), todo[0]))

print('[{0}] [spidy] [INIT]: Starting crawler...'.format(get_time()))
log('LOG: Successfully started crawler.')


#########
## RUN ##
#########

while len(todo) != 0: #While there are links to check
	try:
		if newErrorCount >= maxNewErrors or knownErrorCount >= maxKnownErrors or HTTPErrorCount >= maxHTTPErrors: #If too many errors have occurred
			print('[{0}] [spidy] [ERR]: Too many errors have accumulated, stopping crawler.'.format(get_time()))
			save_files(words)
			sys.exit()
		elif counter >= saveCount: #If it's time for an autosave
			try:
				print('[{0}] [spidy] [LOG]: Queried {1} links. Saving files...'.format(get_time(), str(counter)))
				save_files(words)
				info_log()
				if zipFiles:
					zip(t.time(), 'saved/')
			finally:
				#Reset variables
				counter = 0
				words.clear()
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
			links = (list(set(links))) #Remove duplicates and shuffle links
			for link in links: #Check for invalid links
				if check_link(link):
					links.remove(link)
					removedCount += 1
				link = link.encode('utf-8', 'ignore') #Encode each link to UTF-8 to minimize errors
			todo += links #Add scraped links to the TODO list
			done.append(todo[0]) #Add crawled link to done list
			save_page(todo[0])
			print('[{0}] [spidy] [CRAWL]: Found {1} links and {2} words on {3}'.format(get_time(), len(wordList), len(links), todo[0])) #Announce which link was crawled
			del todo[0]#Remove crawled link from TODO list
			counter += 1
	
	#ERROR HANDLING
	except KeyboardInterrupt: #If the user does ^C
		print('[{0}] [spidy] [ERR]: User performed a KeyboardInterrupt, stopping crawler...'.format(get_time()))
		log('\nLOG: User performed a KeyboardInterrupt, stopping crawler.')
		save_files(words)
		sys.exit()
	except Exception as e:
		link = todo[0].encode('utf-8', 'ignore')
		badLinks.add(link)
		err_print(link)
		errMRO = type(e).mro()
		
		if urllib.error.HTTPError in errMRO: #Bad HTTP Response
			HTTPErrorCount += 1
			print('[{0}] [spidy] [ERR]: Bad HTTP response.'.format(get_time()))
			err_log(link, 'Bad Response', e)
		
		#Other errors
		elif etree.XMLSyntaxError in errMRO or etree.ParserError in errMRO: #Error processing html/xml
			knownErrorCount += 1
			print('[{0}] [spidy] [ERR]: An XMLSyntaxError occured. A web dev screwed up somewhere.'.format(get_time()))
			err_log(link, 'XMLSyntaxError', e)
		
		elif UnicodeError in errMRO: #Error trying to convert foreign characters to Unicode
			knownErrorCount += 1
			print('[{0}] [spidy] [ERR]: A UnicodeError occurred. URL had a foreign character or something.'.format(get_time()))
			err_log(link, 'UnicodeError', e)
		
		elif requests.exceptions.SSLError in errMRO: #Invalid SSL certificate
			knownErrorCount += 1
			print('[{0}] [spidy] [ERR]: An SSLError occured. Site is using an invalid certificate.'.format(get_time()))
			err_log(link, 'SSLError', e)
		
		elif requests.exceptions.ConnectionError in errMRO: #Error connecting to page
			knownErrorCount += 1
			print('[{0}] [spidy] [ERR]: A ConnectionError occurred. There is something wrong with somebody\'s network.'.format(get_time()))
			err_log(link, 'ConnectionError', e)
		
		elif requests.exceptions.TooManyRedirects in errMRO: #Exceeded 30 redirects.
			knownErrorCount += 1
			print('[{0}] [spidy] [ERR]: A TooManyRedirects error occurred. Page is probably part of a redirect loop.'.format(get_time()))
			err_log(link, 'TooManyRedirects', e)
		
		elif requests.exceptions.ContentDecodingError in errMRO: #Received response with content-encoding: gzip, but failed to decode it.
			knownErrorCount += 1
			print('[{0}] [spidy] [ERR]: A ContentDecodingError occurred. Probably just a zip bomb, nothing to worry about.'.format(get_time()))
			err_log(link, 'ContentDecodingError', e)
		
		elif OSError in errMRO:
			knownErrorCount += 1
			print('[{0}] [spidy] [ERR]: An OSError occurred.'.format(get_time()))
			err_log(link, 'OSError', e)
		
		else: #Any other error
			newErrorCount += 1
			print('[{0}] [spidy] [ERR]: An unknown error happened. New debugging material!'.format(get_time()))
			err_log(link, 'Unknown', e)
			if raiseErrors:
				raise
			else:
				continue
		
		err_saved_message()
		del todo[0]
		counter += 1
	finally:
		todo = list(set(todo)) #Removes duplicates and shuffles links so trees don't form.
		#For debugging purposes; to check one link and then stop
		# save_files(words)
		# sys.exit()

print('[{0}] [spidy] [GOD]: How the hell did this happen? I think you\'ve managed to download the internet. I guess you\'ll want to save your files...'.format(get_time()))
save_files(words)