#!/usr/bin/env python

import os
import sys
import socket
import time
import urllib2
import urllib3
import Queue
import threading

from crawler_thread import *

class crawler():
	def __init__(self, max_io = 10, max_parser = 2, request_rate = 500):
		self.access_history = {}
		self.max_io = max_io
		self.max_parser = max_parser
		self.request_rate = request_rate
		self.io_queue = Queue.Queue()
		self.parser_queue = Queue.Queue()
		self.method = 'urllib3'
		for i in range(self.max_io):
			t = crawler_thread(self.io_run, self.io_queue, self.parser_queue)
			t.setDaemon(True)
			t.start()
		for i in range(self.max_parser):
			t = crawler_thread(self.parser_run, self.io_queue, self.parser_queue)
			t.setDaemon(True)
			t.start()

		socket.setdefaulttimeout(20)

	def urllib2_read(self, job):
		response = urllib2.urlopen(job.host + job.get_url())
		job.set_content(response.read())

	def urllib3_read(self, conn, job):
		#print threading.currentThread().getName(), '>', conn.__repr__(), job.host
		response = conn.urlopen('GET', job.get_url(), redirect=True, timeout=20)
		job.set_content(response.data)

	def io_run(self):
		pool = urllib3.PoolManager()
		while True:
			job = self.io_queue.get()
			while job.finish == False:
				try:
					beg = time.time()
					if self.method == 'urllib2':
						self.urllib2_read(job)
					else:
						conn = pool.connection_from_url(job.host)
						self.urllib3_read(conn, job)

					job.elapsed = time.time() - beg
					job.finish = True

					self.parser_queue.put(job)
				except Exception, err:
					print 'io_thread> err %s'%(err)
					job.onfailure()

	def parser_run(self):
		while True:
			job = self.parser_queue.get()
			job.onsuccess()
			self.parser_queue.task_done()
			self.io_queue.task_done()

	def put(self, job):
		key = job.host + job.url
		if  key not in self.access_history:
			self.access_history[key] = True
			self.io_queue.put(job)

	def join(self):
		self.io_queue.join()
		self.parser_queue.join()

	def set_method(self, method):
		self.method = method
