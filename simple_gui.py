from tkinter import *
import time as t
from multiprocessing import Process


def setup_window():
	global window
	print('Configuring window.')
	window.title('WORK')
	# Add window elements and configure


def go():
	global window
	setup_window()
	print('Done configuring window')
	window.mainloop()


def keep_alive():
	global window
	t.sleep(3)
	print('Starting loop')
	while True:
		window.update()


print('Creating window.')
window = Tk()


if __name__ == '__main__':
	print('Making p1')
	p1 = Process(target=go)
	print('Making p2')
	p2 = Process(target=keep_alive)
	print('p1 start')
	p1.start()
	print('p2 start')
	p2.start()
	print('No more processes')
	exit()
