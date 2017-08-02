"""
Compares all lines in a given file and removes duplicates.
"""

import sys

file_name = 'crawler_words.txt'

try:
	file_name = sys.argv[1]
except IndexError:
	print('You didn\'t supply a valid filename.')
	exit()

with open(file_name, 'r') as f:
	file = f.readlines()

wordList = []
badList = []

for line in file:
	if line in wordList:
		badList.append(line)
	else:
		wordList.append(line)

file = open(file_name, 'w')

for line in wordList:
	file.write(line)

file.close()

print('{0} duplicate lines removed from {1}.'.format(len(badList), file_name))
