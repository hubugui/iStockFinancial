#!/usr/bin/env python
#coding:gbk

import os
import sys
import json
import re
import Queue
import threading

from stock import *
from job import *

class industry(job):
	INDUSTRY_URL = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=10000&sort=symbol&asc=1&node=%s&_s_r_a=auto'

	def __init__(self, name='nongye', code='hangye_za01'):
		job.__init__(self, name, self.INDUSTRY_URL%(code), self.onsuccess, self.onfailure, 'industry')
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

	def onsuccess(self, content):
		self.content = self.preprocess(content)

		stocks = json.loads(self.content, encoding="gbk")
		print '.',

		for i, element in enumerate(stocks):
			job = stock(self.get_year(), element["symbol"], element["code"], element["name"])
			self.stocks.append(job)

	def onfailure(self):
		print ''
		print 'industry %03d.%s, failure %s'%(self.idx, self.name, self.url)

	def get_fs(self, home='.'):
		dir = '%s/%s'%(home, self.get_year())
		if not os.path.exists(dir):
			os.mkdir(dir)
		path = '%s/%s.js'%(dir, self.code)

		return dir, path

	def save(self, home='.'):
		dir, path = self.get_fs(home)
		if not os.path.exists(dir):
			os.mkdir(dir)

		fd = open(path, 'wb')

		json_string = u"var %s = {'code':'%s', 'name':'%s', 'stocks':["%(self.code, self.code, self.name)

		for i, stock in enumerate(self.stocks):
			json_string += "{'symbol':'%s', 'name':'%s', 'financial':["%(stock.symbol, stock.name)

			for key, value in sorted(stock.get_values().iteritems()):
				key_pack = key.split(key_separator)

				json_string += "'" + str(value) + "',"

			json_string += ']}, '

		json_string += "]}"

		fd.write(json_string.encode('utf-8'))
		fd.close()

	def exist(self, home='.'):
		dir, path = self.get_fs(home)
		return os.path.isfile(path)
