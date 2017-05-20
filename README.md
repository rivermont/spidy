# web-crawler
A simple to use command line web crawler that saves all visited website links to a folder along with all valid archived links

# how it works
This web crawler is very simple in that the main functionality is it's ability to parse the html for all links and then adds all of those links that are valid into a list called todo. As you would expect the crawler then goes on to do this same process for all links in todo. After every  1000 links queried (by default) the crawler will autosave the done file and will prune the links for any invalid ones.

# error handling and management
While testing we have come across many common errors that aren't easily avoided such as http timeout, unicode encode errors, exceeding maximum redirects, http connection, and document empty(going to picture etc.) For all of these errors we have separate error handling that prints a relevant sttatement to the console since most of these errors are impossible to avoid we just continue past them. For unknown errors we have a cap which will cause the program to stop if we exceed that set amount.
