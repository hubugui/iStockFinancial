#!/usr/bin/env python
#coding:gbk

import os
import json
import re
import sys

sys.path.append('././')

from common.util import *
from crawler import *
from database import *
from job import *
from setting import *
from stock import *

class industry(job):
	HOST = 'http://money.finance.sina.com.cn'
	URL = '/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=10000&sort=symbol&asc=1&node=%s&_s_r_a=auto'

	def __init__(self, name='nongye', code='hangye_za01', pid=0):
		job.__init__(self, name, self.HOST, self.URL%(code), self.onsuccess, self.onfailure, 'industry')
		self.code = code
		self.id = 0
		self.pid = pid
		self.stocks = []
		self.elapsed = 0
		self.stocks_json = ''

	def adjust(self):
		# replace ticktime error
		self.content = re.sub(r'\d+:\d+:\d+', '', self.content)
	 	# adjust json format
		self.content = re.sub(r"{\s*(\w)", r'{"\1', self.content)
		self.content = re.sub(r",\s*(\w)", r',"\1', self.content)
		self.content = re.sub(r"(\w):", r'\1":', self.content)

	def onsuccess(self):
		if self.content == 'null':
			print '^',
		else:
			print '.',
			self.adjust()
			self.stocks_json = json.loads(self.content, encoding="gbk")

	def onfailure(self):
		print ''
		print '%03d. %s %s, failure'%(self.idx, self.code, self.name)

	'''
	def fs(self, home='.'):
		dir = '%s/%s'%(home, self.year)
		if not os.path.exists(dir):
			os.mkdir(dir)
		path = '%s/%s.js'%(dir, self.code)
		return dir, path

	def save(self, home='.'):
		dir, path = self.fs(home)
		if not os.path.exists(dir):
			os.mkdir(dir)
		fd = open(path, 'wb')

		json_string = u"var %s = {'code':'%s', 'name':'%s', 'stocks':["%(self.code, self.code, self.name)

		for i, stock in enumerate(self.stocks):
			if stock.finish == True:
				json_string += "{'symbol':'%s', 'name':'%s', 'financial':["%(stock.symbol, stock.name)

				for key, value in sorted(stock.get_values().iteritems()):
					key_pack = key.split(key_separator)
					json_string += "'" + str(value) + "',"
				json_string += ']}, '
			else:
				print 'fatal error, %s is not finish'%(stock.name)
				sys.exit(0)
			self.elapsed += stock.elapsed

		json_string += "]}"

		fd.write(json_string.encode('utf-8'))
		fd.close()	

	def exist(self, home='.'):
		dir, path = self.fs(home)

		if os.path.isfile(path):
			statinfo = os.stat(path)
			if statinfo.st_size > 0:
				return True
			else:
				return False
		else:
			return False
	'''
