#!/usr/bin/env python

import Queue
import threading

class crawler_thread(threading.Thread):
	def __init__(self, run, io_queue, parser_queue):
		threading.Thread.__init__(self)
		self.io_queue = io_queue
		self.parser_queue = parser_queue
		self.run = run
