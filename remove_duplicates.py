'''
Dupecheck.py
Compares all lines in a given file and removes duplicates.
'''

import sys

try:
	fileName = sys.argv[1]
except:
	print('You didn\'t supply a valid filename.')
	exit()

with open(fileName, 'r') as f:
	file = f.readlines()

wordList = []
badList = []

for line in file:
	if line in wordList:
		badList.append(line)
	else:
		wordList.append(line)

file = open(fileName, 'w')

for line in wordList:
	file.write(line)

file.close()

print('{0} duplicate lines removed from {1}.'.format(len(badList), fileName))
