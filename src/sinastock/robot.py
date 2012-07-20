#!/usr/bin/env python

import os
import sys
import time
import Queue
import threading
import socket

from industry import *
from market_center import *
from stock import *
from thread_url import *

class robot:
	concurrency = 10
 
	def __init__(self, year='2011', home='.'):
		self.year = year
		self.home = home
		self.queue = Queue.Queue(1000)

		for i in range(self.concurrency):
			t = thread_url(self.queue)
			t.setDaemon(True)
			t.start()

	def get_time(self, t):
		return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))

	def fire(self):
		socket.setdefaulttimeout(5)

		# martet
		market = market_center()
		market.pull()
		market.save_js(self.home)

		# csrc industrys
		industrys = market.get_csrc_industrys()
		for i, ind in enumerate(industrys):
			ind.set_idx(i + 1)
			ind.set_year(self.year)
			self.queue.put(ind)

		print '%s> waiting for pull csrc industry, number=%d'%(self.get_time(time.time()), len(industrys))

		self.queue.join()

		print ''		
		print '%s> pull over'%(self.get_time(time.time()))

		# stocks
		idx = 1
		for i, ind in enumerate(industrys):
			print '%03d.%s, %d'%(i + 1, ind.name, len(ind.stocks))

			for j, stock in enumerate(ind.stocks):
				stock.set_idx(idx)
				idx += 1

				self.queue.put(stock)

			self.queue.join()

	def go(self):
		go_t = time.time()
		print '%s> robot go'%(self.get_time(go_t))

		self.fire()

		bye_t = time.time()
		print '%s> byebye'%(self.get_time(bye_t))
		print 'elapsed time %ds'%(bye_t - go_t)
