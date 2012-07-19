#!/usr/bin/env python
#coding:gbk

import os
import sys
from job import *

class stock(job):
	STOCK_URL = 'http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/%s/ctrl/%s/displaytype/4.phtml'

	def __init__(self, year='2011', home='.', name='中金黄金', code='600489'):
		job.__init__(self, name, self.STOCK_URL%(code, year), self.onsuccess, self.onfailure, 'stock')
		self.year = year
		self.home = home
		self.name = name
		self.code = code

	def onsuccess(self, web_data):
		parser = stock_parser()
		parser.parse(html, values)
		parser.close()

	def onfailure(self):
		print self.name + '\tonfailure'
		sys.exit(0)
