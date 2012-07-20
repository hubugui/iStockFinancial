#!/usr/bin/env python

import os
import sys
import time
import urllib2
import urllib3
import Queue
import threading

class thread_url(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run(self):
		http = urllib3.PoolManager(10)

		while True:
			content = ''

			try:
				job = self.queue.get()
				# response = urllib2.urlopen(urllib2.Request(job.url))
				# content = response.read()
				# response.close()

				request = http.request('GET', job.url)
				content = request.data

				if content != 'null':
					job.onsuccess(content)

				self.queue.task_done()
			except Exception, err:
				print err

				job.onfailure()
				self.queue.put(job)
