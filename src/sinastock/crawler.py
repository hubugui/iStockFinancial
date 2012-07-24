#!/usr/bin/env python

import os
import sys
import time
import urllib2
import Queue
import threading

from crawler_thread import *

class crawler():
	def __init__(self, max_io = 10, max_parser = 2, request_rate = 500):
		self.max_io = max_io
		self.max_parser = max_parser
		self.request_rate = request_rate

		self.io_queue = Queue.Queue(100)
		self.parser_queue = Queue.Queue(100)

		for i in range(self.max_io):
			t = crawler_thread(self.io_run, self.io_queue, self.parser_queue)
			t.setDaemon(True)
			t.start()

		for i in range(self.max_parser):
			t = crawler_thread(self.parser_run, self.io_queue, self.parser_queue)
			t.setDaemon(True)
			t.start()

	def io_run(self):
		while True:
			job = None

			try:
				# print '%s bef'%(threading.currentThread().getName())
				job = self.io_queue.get()

				response = urllib2.urlopen(urllib2.Request(job.get_url()))
				job.set_content(response.read())
				response.close()

				job.finish = True
			except Exception, err:
				print ''
				print 'io_thread> err %s'%(err)
				job.onfailure()

			self.parser_queue.put(job)
			self.io_queue.task_done()

	def parser_run(self):
		while True:
			job = None

			try:
				job = self.parser_queue.get()

				if job.finish == True:
					job.onsuccess()
				else:
					self.io_queue.put(job)

				self.parser_queue.task_done()
			except Exception, err:
				print ''
				print 'parser_thread> err %s'%(err)

	def put(self, job):
		self.io_queue.put(job)

	def join(self):
		self.io_queue.join()
		self.parser_queue.join()
