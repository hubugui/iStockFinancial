#!/usr/bin/env python
#coding:gbk

import os
import json
import re
import sys

from stock import *
from job import *

class industry(job):
	INDUSTRY_HOST = 'http://vip.stock.finance.sina.com.cn'
	INDUSTRY_URL = '/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=10000&sort=symbol&asc=1&node=%s&_s_r_a=auto'

	def __init__(self, name='nongye', code='hangye_za01'):
		job.__init__(self, name, self.INDUSTRY_HOST, self.INDUSTRY_URL%(code), self.onsuccess, self.onfailure, 'industry')
		self.code = code
		self.content = ''
		self.stocks = []

	def preprocess(self, content):
		# replace ticktime error
		content = re.sub(r'\d+:\d+:\d+', '', content)

	 	# adjust json format
		content = re.sub(r"{\s*(\w)", r'{"\1', content)
		content = re.sub(r",\s*(\w)", r',"\1', content)
		content = re.sub(r"(\w):", r'\1":', content)

		return content

	def onsuccess(self):
		if self.content == 'null':
			print '^',
		else:
			self.content = self.preprocess(self.content)

			stocks = json.loads(self.content, encoding="gbk")
			print '.',

			for i, element in enumerate(stocks):
				job = stock(self.get_year(), element["symbol"], element["code"], element["name"])
				self.stocks.append(job)

	def onfailure(self):
		print ''
		print '%03d. %s %s, failure'%(self.idx, self.code, self.name)

	def fs(self, home='.'):
		dir = '%s/%s'%(home, self.get_year())
		if not os.path.exists(dir):
			os.mkdir(dir)
		path = '%s/%s.js'%(dir, self.code)

		return dir, path

	def save(self, home='.'):
		elapsed = 0

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

			elapsed += stock.elapsed

		json_string += "]}"

		fd.write(json_string.encode('utf-8'))
		fd.close()

		print 'elapsed %ds'%(elapsed)

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
