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
	def __init__(self, max_io = 10, max_parser = 2, request_rate = 500, proxy = ''):
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

		socket.setdefaulttimeout(20)
		#ip = socket.gethostbyname(socket.gethostname())
		#if ip.startswith('137.'):
		#	self.http_pool = HTTPConnectionPool('10.77.8.70:8080', maxsize = max_io)
		#else:
		#	self.http_pool = HTTPConnectionPool('vip.stock.finance.sina.com.cn', maxsize = max_io)

		self.http = urllib3.PoolManager(maxsize = max_io)

	def urllib2_read(self, job):
		response = urllib2.urlopen(urllib2.Request(job.host + job.get_url()))
		job.set_content(response.read())
		response.close()

	def urllib3_read(self, job):
		url_pools = self.http.connection_from_url(job.host)
		response = url_pools.urlopen('GET', job.get_url(), redirect=True)
		job.set_content(response.data)

	def io_run(self):
		while True:
			job = self.io_queue.get()

			try:
				beg = time.time()
			
				urllib2_read(job)
				# urllib3_read(job)

				job.elapsed = time.time() - beg
				job.finish = True
			except Exception, err:
				print ''
				print 'io_thread> err %s'%(err)
				job.onfailure()

			self.parser_queue.put(job)
			self.io_queue.task_done()

	def parser_run(self):
		while True:
			job = self.parser_queue.get()

			if job.finish == True:
				job.onsuccess()
			else:
				self.io_queue.put(job)

			self.parser_queue.task_done()

	def put(self, job):
		self.io_queue.put(job)

	def join(self):
		while True:
			self.io_queue.join()
			self.parser_queue.join()

			if self.io_queue.qsize() == 0 and self.parser_queue.qsize() == 0:
				break			
