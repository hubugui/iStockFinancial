#!/usr/bin/env python
#coding:gbk

import os
import sys
import threading

from job import *
from stock_parser import *

class stock(job):
	STOCK_URL = 'http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/%s/ctrl/%s/displaytype/4.phtml'

	def __init__(self, year, symbol='sz600489', code='600489', name='中金黄金'):
		job.__init__(self, name, self.STOCK_URL%(code, year), self.onsuccess, self.onfailure, 'stock')
		job.year = year
		self.symbol = symbol
		self.code = code

	def get_values(self):
		return self.values

	def onsuccess(self, content):
		print '%03d. %s %s'%(self.idx, self.code, self.name)

		self.values = {}

		parser = stock_parser()
		parser.parse(content, self.values)
		parser.close()

		# self.write_console(self.values)

	def onfailure(self):
		print ''
		print 'stock %03d.%s, failure %s'%(self.idx, self.name, self.url)
