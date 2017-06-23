'''
Profile module for spdy Web Crawler.
Built by rivermont and FalconWarriorr
'''

import time as t
START_TIME = int(t.time())
def get_time():
	return t.strftime('%H:%M:%S')

print('[{0}] [spidy] [PROFILE]: Importing required libraries...'.format(get_time()))

import cProfile
import pstats
import crawler

cProfile.run('crawler.main()', 'profile.txt')

profile = pstats.Stats('profile.txt')

p.strip_dirs().sort_stats('cumulative').print_stats()
