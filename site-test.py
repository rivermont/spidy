from lxml import html
import msvcrt
import time
import requests
import sys

def start():
    #initializing variables
    print('[INIT]: Creating variables...')
    count = 0;
    errors = 0
    knownErrors = 0
    print('Enter automatic save interval')
    try:
        saveCount = sys.argv[1]
    except:
        saveCount = 1000
        pass
    print('Enter valid non-empty link file for todo')
    try:
        todoFile = sys.argv[2]
    except:
        todoFile = 'crawler_todo.txt'
        pass
    print('Enter valid text file for done')
    try:
        doneFile = sys.argv[3]
    except:
        doneFile = 'crawler_done.txt'
        pass
    print('Enter valid text file for log')
    try:
        logFile = sys.argv[4]
    except:
        logFile = 'crawler_log.txt'
        pass
    print('Enter True if you want to clear the done file')
    clear = input()
    print('Enter True if you want to clear todo and add wikipedia main page')
    clearTodo = input()

    print('[INIT]: Opening saved files')
    #open saved todo file
    with open(todoFile, 'r+') as f:
        if clearTodo == 'True':
            f.write('')
        todo = f.readlines()
    todo = [x.strip() for x in todo]

    #opens all done pages
    with open(doneFile, 'r+') as f:
        #clears doneFile if clear is True
        if clear == 'True':
            print('[INIT]: clearing done file')
            f.write('')
        done = f.readlines()
    done = [x.strip() for x in done]

    #initializes todoFile with default start website
    todo.append('https://en.wikipedia.org/wiki/Main_Page')
    return todo, done, count, errors, knownErrors, doneFile, todoFile, logFile

#defines prune function to delete invalid links
def prune():
    print('[LOG]: Pruning todo files')
    counter = 0;
    for link in todo:
        if link in done:
            counter += 1;
            todo.remove(link)
        elif link[0] != 'h':
            counter += 1;
            todo.remove(link)
        elif len(link) < 7:
            counter += 1
            todo.remove(link)
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
    print('[LOG]: Saving todo to todo file(crawler_todo.txt by default)')
    print('[LOG]: Saving done to done file(crawler_dont.txt by default)')
    doneList = open(doneFile, 'w')
    todoList = open(todoFile, 'w')
    todoList.seek(0)
    doneList.seek(0)
    for site in done: #adds all done sites into saved done file
            doneList.write(str(site.encode('utf-8')) + '\n')
    for site in todo: #adds all todo sites into saved todo file
            todoList.write(str(site.encode('utf-8')) + '\n')
    doneList.close()
    todoList.close()

#called when u key is pressed
def update():
    count = 0
    print('updating logs...')
    save()

#called when s key is pressed
def status():
    print('[LOG] Links in done: ' + str(len(done)))
    print('[LOG] Links in todo: ' + str(len(todo)))

#called when p key is pressed
def pause():
    command = ' '
    while command != '' and command != 'r':
        command = input('Press enter to resume or u, s, r, or e and then enter to update, get status, restart, or prune todo\n')
        if(command == 'u'):
            update()
        elif command == 's':
            status()
        elif command == 'r':
            restart()
        elif command == 'e':
            prune()
        elif command == '':
            print('[LOG]: Resuming crawl')

#called when r key is pressed
def restart():
    start()
todo, done, count, errors, knownErrors, doneFile, todoFile, logFile = start()
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
                print('[CRAWL] Web Crawler currently at: ' + str(todo[0].encode('utf-8'))) #prints current website to the console
                page = requests.get(todo[0])
                done.append(todo[0]) #moves the current website from todo into done
                todo.remove(todo[0])
                tree = html.fromstring(page.content)
                links = tree.xpath('//a/@href') #parses the html for all links
                for item in list(links):
                    item = item.encode('utf-8') #adds all links into todo separately
                todo += list(links)
                todo = list(set(todo)) #removes duplicates and also disorders the list
        else:
            todo.remove(todo[0]) #removes too short links


    #ending the script safely with KeyboardInterrupt        
    except KeyboardInterrupt:
        save()
        exit()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        knownErrors += 1
        print('[ERR]: A connection error occured with link: ' + todo[0] + ', the link may be down.')
        log(e)
        err_saved_message()
    except requests.exceptions.HTTPError as e:
        knownErrors += 1
        print('[ERR]: An HTTPError occured with link: ' + todo[0] + ', there is probably something wrong with the link.')
        log(e)
        err_saved_message()
    except UnicodeEncodeError as e:
        knownErrors += 1
        log(e)
        print('[ERROR]: Unicode Error with link: ' + todo[0] + ', probably a foreign character in the link title.')
        print('[LOG]: Saved error to crawler_log.txt')
        pass        
    except Exception as e: #If any other error is raised
        log(e)
        errors += 1
        print('[ERROR]: An error occured with link: ' + todo[0] + ' probably http related, Saved to log file(crawler_log.txt by default)') #Print in cmd that an error happened
        todo.remove(todo[0]) #Remove unliked link from todo
        continue #Keep going like nothing happened
    #autosaves
    if count > 1000:
        count =0;
        logFile = open(logFile, 'a')
        logFile.write('[AUTOSAVE]: Saved done and todo to crawler_done.txt and crawler_todo.txt by default \n')
        logFile.write('[AUTOSAVE]: Done length: ' + str(len(done) + '\n'))
        logFile.write('[AUTOSAVE]: Todo length: ' + str(len(todo) + '\n\n\n'))
        logFile.close()
        print('[LOG]: Queried 1000 websites, Automatically saving done and todo files')
        save()    
print('Internet has been mastered')
