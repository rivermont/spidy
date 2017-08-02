"""
Wordlist post-processing
"""


import sys

wordFile = sys.argv[1]

with open(wordFile, 'r') as f:
	file = f.readlines()

file = [x.strip() for x in file]

file = list(set(file))


def check_word(word):
	"""
	Returns True if word in not valid
	Returns False if word is valid
	"""
	if len(word) > 16:
		return True
	else: 
		return False


def run():
	before = len(file)

	for word in file:
		if check_word(word):
			file.remove(word)

	removed = before - len(file)

	save_file = open(wordFile, 'w')

	for line in file:
		save_file.write('\n' + line)

	save_file.close()

	print('Removed {0} links from {1}'.format(removed, wordFile))

run()
run()
run()
run()
