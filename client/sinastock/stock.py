#!/usr/bin/env python
#coding:gbk

from job import *
from stock_parser import *
from industry import *

class stock(job):
	STOCK_HOST = 'money.finance.sina.com.cn'
	STOCK_URL = '/corp/go.php/vFD_FinancialGuideLine/stockid/%s/ctrl/%s/displaytype/4.phtml'

	def __init__(self, year, symbol='sz600489', code='600489', name='中金黄金', industry=None):
		job.__init__(self, name, self.STOCK_HOST, self.STOCK_URL%(code, year), self.onsuccess, self.onfailure, 'stock')
		job.year = year
		self.symbol = symbol
		self.code = code
		self.industry = industry

	def get_values(self):
		return self.values

	def onsuccess(self):
		print '%03d. %s %s'%(self.idx, self.code, self.name)

		self.values = {}

		parser = stock_parser()
		parser.parse(self.content, self.values)
		parser.close()

		self.industry.onstock_done(self)

	def onfailure(self):
		print ''
		print '%03d. %s %s, failure'%(self.idx, self.code, self.name)
