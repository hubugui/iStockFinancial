#!/usr/bin/env python
#coding:gbk

import os
import sys
import urllib2
import json
import re

from industry import *
from job import *
from setting import *

class market_center(job):
	MARKET_HOST = 'http://money.finance.sina.com.cn'
	MARKET_URL = '/quotes_service/api/json_v2.php/Market_Center.getHQNodes'

	def __init__(self):
		job.__init__(self, 'market', self.MARKET_HOST, self.MARKET_URL, self.onsuccess, self.onfailure, 'market')
		self.json = ''
		self.industrys = []

	def save(self, home='.'):
		fd = open(home + '/market_center.js', 'wb')
		fd.write('var tree = ' + self.content + ';');
		fd.close()

	def adjust(self):
		# adjust js array to json
		self.content = re.sub(r"{\s*(\w)", r'{"\1', self.content)
		self.content = re.sub(r",\s*(\w)", r',"\1', self.content)
		self.content = re.sub(r"(\w):", r'\1":', self.content)
	 	# "{node: \'sh_z\'}"
		self.content = re.sub(r"\"{", r"{", self.content)
		self.content = re.sub(r"}\"", r"}", self.content)
		self.content = re.sub(r"\\'", r'"', self.content)
	 	# ["<font color="red">条件选股<\/font>","http":\/\/screener.finance.sina.com.cn\/index.html?f=hqcenter","hsgs_tjxg","",{"linktype":\"_blank\"}]
		self.content = re.sub(r'"red"', r'red', self.content)
		self.content = re.sub(r'<\\/font>', r'', self.content)
		self.content = re.sub(r'http"', r'', self.content)	
		self.content = re.sub(r'\\"', r'"', self.content)
		# ["板块汇总行情","frames\/sl_bk.html","bkhq","null,{"linktype":"iframe"}]
		self.content = re.sub(r'"null,', r'"null",', self.content)

	def onsuccess(self):
		print '%s'%(self.name)

		self.adjust()
		self.json = json.loads(self.content, encoding="gbk")
		self.csrc_recursion(self.json[1][0][1][3], 0, '')

	def onfailure(self):
		print '%s, failure'%(self.name)

	def echo(self, msg, level):
		for i in range(level):
			print '    ',
		print msg

	# CSRC(China Securities Regulatory Commission) Industry
	def csrc_recursion(self, array, level, parent_name):
		ind = None
		if len(array[1]) == 0:
			ind = industry(array[0], array[2], parent_name)
			msg = array[0] + '-' + array[2]
		else:
			ind = industry(array[0], '', parent_name)
			msg = array[0] + '-' + str(len(array[1]))
		self.echo(msg, level)

		setting['db'].industry_add(ind)

		for element in array[1]:
			if isinstance(element, (list, tuple)):
				self.csrc_recursion(element, level + 1, array[0])

				if not isinstance(element[1], (list, tuple)):
					ind = industry(element[0], element[2], array[0])
					self.industrys.append(ind)

	def get_csrc_industrys(self):
		return self.industrys
