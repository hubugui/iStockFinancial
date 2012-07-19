#!/usr/bin/env python

import os
import sys
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

			try:
				job = self.queue.get()

				req = urllib2.Request(job.url)
				response = urllib2.urlopen(req)
				content = response.read()
				response.close()

				if content != 'null':
					job.onsuccess(content)
			except:
				print "Unexpected error:", sys.exc_info()[1]
				print content
				job.onfailure()

			self.queue.task_done()
