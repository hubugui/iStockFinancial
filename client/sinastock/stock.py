#!/usr/bin/env python
#coding:gbk

from industry import *
from job import *
from setting import *
from stock_parser import *

class stock(job):
	HOST = 'http://money.finance.sina.com.cn'
	URL = '/corp/go.php/vFD_FinancialGuideLine/stockid/%s/ctrl/%d/displaytype/4.phtml'

	def __init__(self, year, symbol='sz600489', code='600489', name='中金黄金'):
		job.__init__(self, name, self.HOST, self.URL%(code, year), self.onsuccess, self.onfailure, 'stock')
		job.year = year
		self.symbol = symbol
		self.code = code

	def __repr__(self):
		return self.name, self.symbol, self.year, self.host, self.url

	def get_values(self):
		return self.values

	def onsuccess(self):
		print '%03d. %s %s %s'%(self.idx, self.code, self.name, self.year)

		self.values = {}
		all_year = []

		parser = stock_parser()
		parser.parse(self.content, self.values, all_year)
		parser.close()

		for req_year in setting['years']:
			for per_year in all_year:
				if req_year == int(per_year) and req_year != self.year:
					print req_year, self.year

					new_stock = stock(req_year, self.symbol, self.code, self.name)
					setting['crawler'].put(new_stock)
					# print new_stock.__repr__()

		#if len(self.values) > 0:
		#	save to database

	def onfailure(self):
		print ''
		print '%03d. %s %s %s, failure'%(self.idx, self.code, self.name, self.year)
