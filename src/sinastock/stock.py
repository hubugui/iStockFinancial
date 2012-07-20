#!/usr/bin/env python
#coding:gbk

import os
import sys
import threading

from job import *
from stock_parser import *

class stock(job):
	STOCK_URL = 'http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/%s/ctrl/%s/displaytype/4.phtml'

	def __init__(self, year='2011', code='600489', name='中金黄金'):
		job.__init__(self, name, self.STOCK_URL%(code, year), self.onsuccess, self.onfailure, 'stock')
		self.year = year
		self.code = code

	def write_console(self, values):
		for key, value in sorted(values.iteritems()):
			key_pack = key.split(key_separator)

			print key_pack[0] + "." + key_pack[1] + '=' + str(value)

	def onsuccess(self, content):
		print threading.currentThread().getName() + ' stock ' + str(self.idx) + '.' + self.name

		values = {}

		parser = stock_parser()
		parser.parse(content, values)
		parser.close()

		# self.write_console(values)

	def onfailure(self):
		print self.name + '\tonfailure'
		sys.exit(0)
