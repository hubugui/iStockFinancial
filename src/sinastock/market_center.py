#!/usr/bin/env python
#coding:gbk

import os
import sys
import urllib2
import json
import re

from industry import *

class market_center:
	url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodes'

	def __init__(self):
		self.content = ''
		self.json = ''
		self.industrys = []

	def save_js(self, home='.'):
		fd = open(home + '/market_center.js', 'wb')
		fd.write('var tree = ' + self.content + ';');
		fd.close()

	def preprocess(self, content):
		# adjust js array to json

		content = re.sub(r"{\s*(\w)", r'{"\1', content)
		content = re.sub(r",\s*(\w)", r',"\1', content)
		content = re.sub(r"(\w):", r'\1":', content)
	 	# "{node: \'sh_z\'}"
		content = re.sub(r"\"{", r"{", content)
		content = re.sub(r"}\"", r"}", content)
		content = re.sub(r"\\'", r'"', content)
	 	# ["<font color="red">条件选股<\/font>","http":\/\/screener.finance.sina.com.cn\/index.html?f=hqcenter","hsgs_tjxg","",{"linktype":\"_blank\"}]
		content = re.sub(r'"red"', r'red', content)
		content = re.sub(r'<\\/font>', r'', content)
		content = re.sub(r'http"', r'', content)	
		content = re.sub(r'\\"', r'"', content)
		# ["板块汇总行情","frames\/sl_bk.html","bkhq","null,{"linktype":"iframe"}]
		content = re.sub(r'"null,', r'"null",', content)

		return content

	def pull(self):
		print "pull market_center: " + self.url

		response = urllib2.urlopen(urllib2.Request(self.url))
	 	self.content = self.preprocess(response.read())
		response.close()

		self.json = json.loads(self.content, encoding="gbk")
		self.csrc_recursion(self.json[1][0][1][3], 0)

	def echo(self, msg, level):
		for i in range(level):
			print '    ',
		print msg.encode('gbk')

	'''
		CSRC(China Securities Regulatory Commission) Industry
	'''
	def csrc_recursion(self, array, level):
		'''	
		if len(array[1]) == 0:
			msg = array[0] + '-' + array[2]
		else:
			msg = array[0] + '-' + str(len(array[1]))
		self.echo(msg, level)
		'''

		for element in array[1]:
			if isinstance(element, (list, tuple)):
				self.csrc_recursion(element, level + 1)

				if not isinstance(element[1], (list, tuple)):
					ind = industry(element[0], element[2])
					self.industrys.append(ind)

	def get_csrc_industrys(self):
		return self.industrys
