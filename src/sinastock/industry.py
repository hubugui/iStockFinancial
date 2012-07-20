#!/usr/bin/env python
#coding:gbk

import os
import sys
import urllib2
import json
import re
import Queue
import threading

from stock_parser import key_separator
from stock import *
from job import *

def write_json(values, count, path):
	fd = open(path, 'wb')

	json_string = "{"

	for key, value in sorted(values.iteritems()):
		key_pack = key.split(key_separator)
		json_string += "'" + key_pack[1] + "': " + str(value / count) + ","

	json_string += "}"

	print json.dumps(json_string, encoding="gbk", indent=2)

	json_string = json.dumps(json_string, fp=fd, sort_keys=True, encoding="gbk", indent=2)

	# fd.write(json_string);
	fd.close()

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
			job = stock(self.get_year(), element["code"], element["name"])
			self.stocks.append(job)			

	def onfailure(self):
		print ''
		print self.name + '\tonfailure' + '\t' + self.url
		sys.exit(0)
