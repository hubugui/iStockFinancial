#!/usr/bin/env python

import os
import sys
import time
import Queue
import threading

from industry import *
from industry_list import *
from thread_url import *

'''
	CSRC(China Securities Regulatory Commission) Industry
'''

class robot:
	def __init__(self, year='2011', home='.'):
		self.year = year
		self.home = home
		self.jobs = []
		self.queue = Queue.Queue()

		for i in range(1):
			t = thread_url(self.queue)
			t.setDaemon(True)
			t.start()

	def echo(self, msg, level):
		for i in range(level):
			print '    ',
		print msg.encode('gbk')

	def extract(self, array, level):
		'''	
		if len(array[1]) == 0:
			msg = array[0] + '-' + array[2]
		else:
			msg = array[0] + '-' + str(len(array[1]))
		self.echo(msg, level)
		'''

		for element in array[1]:
			if isinstance(element, (list, tuple)):
				self.extract(element, level + 1)

				if not isinstance(element[1], (list, tuple)):
					ind = industry(self.year, self.home, element[0], element[2])
					self.jobs.append(ind)

	def get_time(self, t):
		return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))

	def go(self):
		go_t = time.time()
		print 'go, %s'%(self.get_time(go_t))

		industrys = industry_list(self.home)
		array = industrys.pull()
		industrys.save()

		self.extract(array[1][0][1][3], 0)

		print 'industry number %d'%(len(self.jobs))

		for i, job in enumerate(self.jobs):
			job.idx = i + 1
			self.queue.put(job)

		self.queue.join()

		bye_t = time.time()
		print 'byebye, %s'%(self.get_time(bye_t))
		print 'elapsed time %ds'%(bye_t - go_t)
