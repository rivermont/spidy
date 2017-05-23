from lxml import html
import msvcrt
import time
import requests
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup

def start():
    #initializing variables
    print('[INIT]: Creating variables...')
    count = 0;
    errors = 0
    knownErrors = 0
    saveCount = 1000
    debug = False
    todoFile = 'crawler_todo.txt'
    doneFile = 'crawler_done.txt'
    logFile = 'crawler_log.txt'
    textFile = 'crawler_text.txt'

    #overrides default files and save count if requested
    custom = input('Would you like to change the default save settings y/n: ')
    if custom == 'y' or custom == 'Y' or custom == 'yes' or custom == 'Yes':
        print('Enter automatic save interval')
        saveCount = input()
        if saveCount == None:
            saveCount = 1000
        print('Enter valid non-empty link file for todo')
        todoFile = input()
        if todoFile == None:
            todoFile = 'crawler_todo.txt'
        print('Enter valid text file for done')
        doneFile = input()
        if doneFile == None:
            doneFile = 'crawler_done.txt'
        print('Enter valid text file for log')
        logFile = input()
        if logFile == None:
            logFile = 'crawler_log.txt'

    #debug mode raises every error if requested
    deb = input('Enter y if you want want to enter debug mode and raise every error\n')
    if deb == 'y':
        debug = True

    #defines vars to clear certain files based on user input
    print('Enter y if you want to clear the done file')
    clear = input()
    print('Enter y if you want to clear todo and add wikipedia main page')
    clearTodo = input()
    print('Enter y if you want to save text from the webpages')
    saveText = input()

    #defines a text file if save text is requested
    if saveText == 'y':
        print('Enter valid text file for text or just press enter to use the default crawler_text.txt')
        textFile = input()
        #used default if no input is given
        if textFile == None or textFile == '':
            textFile = 'crawler_text.txt'
        #defines var to clear text
        print('Enter y if you want to clear the previous text file\n')
        clearText = input()
    else:
        #defines a text list to avoid errors
        text = []
        clearText = ''

    #displays requested info on command prompt
    display = input('Enter a number 0-4 for size of done, size of todo, words in text, total errors, unknown errors to be constantly displayed\n')
    print('[INIT]: Opening saved files')


    #open saved files
    if clearText == 'y':
        with open(textFile, 'w') as f:
            print('[INIT]: Clearing textFile')
            f.write('')
            text = []
    elif saveText == 'y':
        with open(textFile, 'r+') as f:
            print('[INIT]: Opening textFile')
            text = f.readlines()
    #open saved todo file
    if clearTodo == 'y':
        print('[INIT]: Clearing todoFile')
        with open(todoFile, 'w') as f:
            f.write('')
            todo = []
    else:
        with open(todoFile, 'r+') as f:
            print('[INIT]: opening todoFile')
            todo = f.readlines()
            todo = [x.strip() for x in todo]

    #opens all done pages
        #clears doneFile if clear is True
    if clear == 'y':
        with open(doneFile, 'w') as f:
            print('[INIT]: clearing done file')
            f.write('')
            done = []
    else:
        with open(doneFile, 'r+') as f:
            print('[INIT]: opening doneFile')
            done = f.readlines()
            done = [x.strip() for x in todo]

    #initializes todoFile with default start website
    print('[INIT]: Initializing todoFile with wikipedia main page')
    todo.append('https://en.wikipedia.org/wiki/Main_Page')
    return todo, done, count, errors, knownErrors, doneFile, todoFile, logFile, text, textFile, debug, saveCount, saveText, display

#defines prune function to delete invalid links
def prune():
    print('[LOG]: Pruning todo files')
    counter = 0;
    for link in todo:
        if link in done:
            counter += 1;
            todo.remove(link)
        elif len(link) < 7:
            counter += 1
            todo.remove(link)
        elif link[0] != 'h':
            counter += 1;
            todo.remove(link)
    for line in text:
        text.remove(line)
        if line in text:
            pass
        else:
            text.append(line)
    print('Removed ' + str(counter) + ' invalid links')
        
#defines log to log an error into log file
def log(error):
    log = open(logFile, 'a') #Open the log file
    log.seek(0) #Go to the first line
    log.write('\n\nSITE: ' + str(todo[0].encode('utf-8')) + '\nTIME: ' + str(time.time()) + 'ERROR: ' + str(e) + '\n\n') #Write the error message
    log.close()

#defines save to output info to command line and to update done and todo files
def save():
    prune()
    print('[LOG]: Known Errors thrown so far: ' + str(knownErrors))
    print('[LOG]: Errors thrown so far: ' + str(errors))
    print('[LOG]: Links already done: ' + str(len(done)))
    print('[LOG]: Links in todo: ' + str(len(todo)))
    print('[LOG]: number of words in text: ' + str(len(text)))
    doneList = open(doneFile, 'w')
    todoList = open(todoFile, 'w')
    textList = open(textFile, 'w')
    todoList.seek(0)
    doneList.seek(0)
    print('[LOG]: Saving done to done file(crawler_dont.txt by default)')
    for site in done: #adds all done sites into saved done file
            doneList.write(str(site.encode('utf-8')) + '\n')
    print('[LOG]: Saving todo to todo file(crawler_todo.txt by default)')
    for site in todo: #adds all todo sites into saved todo file
            todoList.write(str(site.encode('utf-8')) + '\n')

    #saves text if user selected that option
    if saveText == 'y':
        print('[LOG]: Saving text to text file(crawler_text.txt by default)')
        #iterates through every entry in text and checks to make sure there are no duplicates before adding it to the text file
        for word in text:
            if word != None:
                try:
                    textList.write(str(word.encode('utf-8'))[2:-1] + '\n')
                except:
                    pass
    doneList.close()
    todoList.close()
    textList.close()
#called when u key is pressed
def update():
    count = 0
    print('updating logs...')
    save()

#called when s key is pressed
def status():   #outputs the length of all relevant files
    print('[LOG]: Total errors encountered: ' + str(errors+knownErrors))
    print('[LOG]: Unknown errors encountered: ' + str(errors))
    print('[LOG] Links in done: ' + str(len(done)))
    print('[LOG] Links in todo: ' + str(len(todo)))
    if saveText == '':
        print('[LOG]: Words in text: ' + str(len(text)))

#called when p key is pressed
def pause():
    command = ' '
    #stays paused as long as the input isn't '' or 'r'(restart)
    while command != '' and command != 'r':

        #pause menu
        try:
            command = input('\rPress enter to resume or u, s, r, or e and then enter to update, get status, restart, or prune todo\n')

            #checks to see if any valid command is entered and then executes it
            if(command == 'u'):
                update()
            elif command == 's':
                status()
            elif command == 'r':
                restart()
            elif command == 'e':
                prune()       
        except KeyboardInterrupt:
            save()
            exit()
    print('[LOG]: Resuming crawl')

#called when r key is pressed
def restart():
    save()
    print('\r[RESTART]\n[RESTART]\n[RESTART]: Restarting crawl . . .\n[RESTART]\n[RESTART]\n[RESTART]')
    #calls start to completely start over
    start()
    todo, done, count, errors, knownErrors, doneFile, todoFile, logFile, text, textFile, debug, saveCount, saveText, display = start()

#used to draw keyboard commmands to the bottom of the command prompt
#0-4 for size of done, size of todo, words in text, total errors, unknown errors
def info():
    if display == '0':
        sys.stdout.write("\r" + "Links in done: " + str(len(done)) + " p>pause, u>update, r>restart, e>prune, or s>status")
    if display == '1':
        sys.stdout.write("\r" + "Links in todo: " + str(len(todo)) + " p>pause, u>update, r>restart, e>prune, or s>status")
    if display == '2':
        sys.stdout.write("\r" + "Words in text: " + str(len(text)) + " p>pause, u>update, r>restart, e>prune, or s>status")
    if display == '3':
        sys.stdout.write("\r" + "Total errors: " + str(errors + knownErrors) + " p>pause, u>update, r>restart, e>prune, or s>status")
    if display == '4':
        sys.stdout.write("\r" + "Unknown errors: " + str(errors) + " p>pause, u>update, r>restart, e>prune, or s>status")
    flush()
#flushes the buffer to immediately write the above info to the command prompt
def flush():
    sys.stdout.flush()

#given a link this parses the html on the webpage for the text and outputs it to crawler_text.txt by default with one word per line
def textFromHtml(link):
    flush()
    print('\r[LOG]: Parsing: ' + todo[0] + ' for text\n')
    
    info()
    with urlopen(link) as url:
        html =  url.read()
    soup = BeautifulSoup(html)
    
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    t = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in t.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    #t = '\n'.join(chunk for chunk in chunks if chunk)
    t = t.split()
    for word in t:
        word = str(word.encode('utf-8'))[2:-1]
        if len(word) < 18 and len(word) > 3:
            word.replace("\\", "")
            if word in text:
                pass
            else:
                text.append(word)
    flush()
    
    
todo, done, count, errors, knownErrors, doneFile, todoFile, logFile, text, textFile, debug, saveCount, saveText, display = start()
print('[INIT]: Starting Crawler...')


#loops as long as we haven't mastered the internet
while len(todo) != 0:
    

    #tests for key press
    if msvcrt.kbhit():
        key = msvcrt.getch()

        #updates log if u is pressed
        if key == b'u':
            update()
        elif key == b's':
            status()
        elif key == b'p':
            pause()
        elif key == b'r':
            restart()
        elif key == b'e':
            prune()
                
    try:
        #prevents too short links    
        if len(todo[0]) > 7:
            #prevents invalid links
            if todo[0][0] != 'h':
                todo.remove(todo[0]) #removes invalid links from todo
            elif todo[0] in done:    #removes already done links
                todo.remove(todo[0])

            #actual web crawling process    
            else:
                count += 1
                print('\r[CRAWL] Web Crawler currently at: ' + str(todo[0].encode('utf-8')) + '               ') #prints current website to the console
                info()
                flush()
                page = requests.get(todo[0])
                if saveText == 'y':
                    text.append(textFromHtml(str(todo[0])))
                done.append(todo[0]) #moves the current website from todo into done
                todo.remove(todo[0])
                tree = html.fromstring(page.content)
                links = tree.xpath('//a/@href') #parses the html for all links
                for item in list(links):
                    item = item.encode('utf-8') #adds all links into todo separately
                todo += list(links)
                todo = list(set(todo)) #removes duplicates and also disorders the list
                #prune()
                flush()
        else:
            todo.remove(todo[0]) #removes too short links


    #ending the script safely with KeyboardInterrupt        
    except KeyboardInterrupt:
        save()
        exit()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        if debug:
            save()
            raise
        knownErrors += 1
        print('\r\n[ERR]: A connection error occured with link: ' + todo[0] + ', the link may be down.')
        print('[LOG]: Saved error to ' + logFile + '                             ')
        todo.remove(todo[0])
        log(e)
        
    except requests.exceptions.HTTPError as e:
        if debug:
            save()
            raise
        knownErrors += 1
        print('\r\n[ERR]: An HTTPError occured with link: ' + todo[0] + ', there is probably something wrong with the link.')
        print('[LOG]: Saved error to ' + logFile + '                                ')
        todo.remove(todo[0])
        log(e)
    
    except UnicodeEncodeError as e:
        if debug:
            save()
            raise
        knownErrors += 1
        log(e)
        print('\r\n[ERROR]: Unicode Error with link: ' + todo[0] + ', probably a foreign character in the link title.')
        print('[LOG]: Saved error to ' + logFile + '                                ')
        todo.remove(todo[0])
        pass        
    except Exception as e: #If any other error is raised
        if debug:
            save()
            raise
        log(e)
        errors += 1
        print('\r\n[ERROR]: An error occured with link: ' + todo[0] + ' \nprobably http related, Saved to log file(crawler_log.txt by default)') #Print in cmd that an error happened
        print('[LOG]: Saved error to ' + logFile)
        todo.remove(todo[0]) #Remove unliked link from todo
        pass #Keep going like nothing happened
    
    #autosaves after successfully querying specified number of websites(default 1000)
    if count > int(saveCount):
        count =0;
        logFile = open(logFile, 'a')
        logFile.write('[AUTOSAVE]: Saved done and todo to crawler_done.txt and crawler_todo.txt by default \n')
        logFile.write('[AUTOSAVE]: Done length: ' + str(len(done) + '\n'))
        logFile.write('[AUTOSAVE]: Todo length: ' + str(len(todo) + '\n\n\n'))
        logFile.close()
        print('[LOG]: Queried 1000 websites, Automatically saving done and todo files')
        save()
        info()
        flush()
    info()
    flush()
flush()
print('Internet has been mastered')
