#!/usr/bin/env python

import os
import sys
import time
import urllib2
import Queue
import threading

class thread_url(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run(self):
		while True:
			content = ''

			job = None

			try:
				# print '%s bef'%(threading.currentThread().getName())
				job = self.queue.get()

				response = urllib2.urlopen(urllib2.Request(job.url))
				content = response.read()
				response.close()

				if content != 'null':
					job.onsuccess(content)

				self.queue.task_done()
			except Queue.Empty, err:
				print 'err %s'%(err)
			except Exception, err:
				# print '%s err %s'%(threading.currentThread().getName(), err)
				print 'err %s'%(err)
				job.onfailure()
				self.queue.put(job)
