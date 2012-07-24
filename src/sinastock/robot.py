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
from stock_parser import *
from crawler import *

class robot:
	def __init__(self, year='2011', home='.'):
		self.year = year
		self.home = home
		self.crawler = crawler(20, 2, 500)

	def get_time(self, t):
		return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))

	def save_financial_keys(self):
		# financial data keys
		fd = open(self.home + '/financial_keys.js', 'wb')

		financial_content = 'var financial_keys = ['
		for key in financial_keys:
			financial_content += "'" + key + "',"
		financial_content += '];'

		fd.write(financial_content)
		fd.close()

	def fire(self):
		self.save_financial_keys()

		# martet
		market = market_center()
		market.pull()
		market.save_js(self.home)

		# csrc industrys
		industrys = market.get_csrc_industrys()
		for i, ind in enumerate(industrys):
			ind.set_idx(i + 1)
			ind.set_year(self.year)
			self.crawler.put(ind)

		print '%s> waiting for pull csrc industry, number=%d'%(self.get_time(time.time()), len(industrys))

		self.crawler.join()

		print ''		
		print '%s> over'%(self.get_time(time.time()))

		# stocks
		idx = 1
		for i, ind in enumerate(industrys):
			if ind.exist(self.home):
				print '%03d.%s, %d->already exist'%(i + 1, ind.name, len(ind.stocks))
			else:
				print '%03d.%s, %d'%(i + 1, ind.name, len(ind.stocks))

				for j, stock in enumerate(ind.stocks):
					stock.set_idx(idx)
					idx += 1

					self.crawler.put(stock)
				self.crawler.join()

				ind.save(self.home)

	def go(self):
		go_t = time.time()
		print '%s> robot go'%(self.get_time(go_t))

		socket.setdefaulttimeout(20)
		self.fire()

		bye_t = time.time()
		print '%s> byebye'%(self.get_time(bye_t))
		print 'elapsed time %ds'%(bye_t - go_t)
