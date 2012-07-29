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
from crawler import *

class robot:
	def __init__(self, home='.', year='2011', crawler=None):
		self.home = home
		self.year = year
		self.crawler = crawler

	def get_time(self, t):
		return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))

	def save_financial_keys(self):
		fd = open(self.home + '/financial_keys.js', 'wb')

		financial_content = 'var financial_keys = ['
		for key in financial_keys:
			financial_content += "'" + key + "',"
		financial_content += '];'

		fd.write(financial_content)
		fd.close()

	def fire(self, method):
		self.crawler.set_method(method)
		self.save_financial_keys()

		# martet
		self.market = market_center()
		self.market.pull()
		self.market.save_js(self.home)
		# csrc industrys
		industrys = self.market.get_csrc_industrys()
		for i, ind in enumerate(industrys):
			ind.set_idx(i + 1)
			ind.set_year(self.year)
			ind.set_home(self.home)
			self.crawler.put(ind)

		print '%s> waiting for pull csrc industry, number=%d'%(self.get_time(time.time()), len(industrys))

		self.crawler.join()

		print ''
		print '%s> over'%(self.get_time(time.time()))

		idx = 0
		foreach_num = len(industrys)
		for i, ind in enumerate(industrys):
			if ind.exist(self.home):
				print '%03d.%s, %d->already exist'%(i + 1, ind.name, len(ind.stocks))
			else:
				print '%03d.%s, %d'%(i + 1, ind.name, len(ind.stocks))
				for stock in ind.stocks:
					idx += 1
					stock.set_idx(idx)
					self.crawler.put(stock)
				if i >= foreach_num:
					break

		self.crawler.join()

		print '%s> idx=%d'%(self.get_time(time.time()), idx)

	def go(self):
		elapsed = 0
		methods = ['urllib3']
		for method in methods:
			go_t = time.time()
			print '%s> year %s %s go'%(self.get_time(go_t), self.year, method)

			self.fire(method)

			bye_t = time.time()
			elapsed += bye_t - go_t
			print '%s> year %s %s byebye, elapsed time %ds'%(self.get_time(bye_t), self.year, method, bye_t - go_t)

		return elapsed
