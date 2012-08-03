#!/usr/bin/env python

import os
import sys
import time
import Queue

from crawler import *
from database import *
from industry import *
from job import *
from market_center import *
from setting import *
from stock import *

class robot:
	def get_time(self, t):
		return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))

	def fire_financial_keys(self):
		fd = open(setting['home'] + '/financial_keys.js', 'wb')

		content = 'var financial_keys = ['
		for key in financial_keys:
			content += "'" + key + "',"
		content += '];'

		fd.write(content)
		fd.close()

	def fire_market(self):	
		print '%s> pull market center'%(self.get_time(time.time()))
	
		self.market = market_center()
		setting['crawler'].put(self.market)
		setting['crawler'].join()
		self.market.save(setting['home'])

		print '%s> over'%(self.get_time(time.time()))

	def fire_industry(self):
		self.industrys = self.market.get_csrc_industrys()
		#for industry_idx, ind in enumerate(self.industrys):
		#	ind.set_idx(industry_idx + 1)
		#	setting['crawler'].put(ind)

		print '%s> pull csrc industry, number=%d'%(self.get_time(time.time()), len(self.industrys))

		setting['crawler'].join()

		print ''
		print '%s> over'%(self.get_time(time.time()))

	def fire_stock(self, year):
		industry_idx = 0
		industry_num = 0#len(self.industrys)

		stock_idx = 0
		stock_num = 0
		for industry_idx, ind in enumerate(self.industrys):
			if industry_idx >= industry_num:
				break
			print '%03d.%s, %d'%(industry_idx + 1, ind.name, len(ind.stocks_json))

			for element in ind.stocks_json:
				if stock_idx >= stock_num:
					break
				stock_idx += 1

				job = stock(year, element["symbol"], element["code"], element["name"], ind.id)
				job.set_idx(stock_idx)
				ind.stocks.append(job)
				setting['crawler'].put(job)

		setting['crawler'].join()
		print '%s> over, stock_idx=%d'%(self.get_time(time.time()), stock_idx)

	def go(self):
		setting['db'] = database(setting['home'], 'istock')
		setting['db'].install()

		self.fire_financial_keys()

		year = setting['years'][-1]
		total_elapsed = 0
		for method in ['urllib2']:
			setting['crawler'].set_method(method)

			self.fire_market()
			self.fire_industry()

			elapsed = 0
			beg_t = time.time()
			print '%s> year=%d %s go'%(self.get_time(beg_t), year, method)

			self.fire_stock(year)

			end_t = time.time()
			elapsed = end_t - beg_t
			total_elapsed += elapsed
			print '%s> year=%d %s byebye, elapsed %ds'%(self.get_time(end_t), year, method, elapsed)

		print 'total elapsed %ds'%(total_elapsed)
