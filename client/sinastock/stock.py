#!/usr/bin/env python
#coding:gbk

import threading

from crawler import *
from database import *
from industry import *
from job import *
from setting import *
from stock_parser import *

class stock(job):
	HOST = 'http://money.finance.sina.com.cn'
	URL = '/corp/go.php/vFD_FinancialGuideLine/stockid/%s/ctrl/%d/displaytype/4.phtml'

	def __init__(self, year, symbol='sz600489', code='600489', name='中金黄金', industry_id=-1):
		job.__init__(self, name, self.HOST, self.URL%(code, year), self.onsuccess, self.onfailure, 'stock')		
		self.symbol = symbol
		self.code = code
		self.industry_id = industry_id
		self.set_year(year)

	def __repr__(self):
		return '%03d. %d %s %s'%(self.idx, self.year, self.symbol, self.name)

	def get_values(self):
		return self.values

	def onsuccess(self):
		self.values = {}
		all_year = []

		parser = stock_parser()
		parser.parse(self.content, self.values, all_year)
		parser.close()

		if len(self.values) > 0:
			print '%03d. %d %s %s'%(self.idx, self.year, self.symbol, self.name)

			# crawl prev year
			next_year = self.get_year() - 1
			for req_year in setting['years']:
				if req_year == next_year:
					for per_year in all_year:
						if req_year == int(per_year):
							new_stock = stock(req_year, self.symbol, self.code, self.name, self.industry_id)
							new_stock.set_idx(self.idx)
							setting['crawler'].put(new_stock)
							break

			# save to database
			setting['db'].stock_add(self)
		else:
			print '%03d. %s %s %s, no data'%(self.idx, self.year, self.symbol, self.name)

	def onfailure(self):
		print ''
		print '%03d. %s %s %s, failure'%(self.idx, self.year, self.symbol, self.name)
