#!/usr/bin/env python
#coding:gbk

import os
import sys
import urllib2
import json
import re

class industry_list:
	INDUSTRY_LIST_URL = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodes'

	def __init__(self, home='.'):
		self.home = home
		self.content = ''

	def save(self):
		fd = open(self.home + '/industry_list.js', 'wb')
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
		print "pull industry list: " + self.INDUSTRY_LIST_URL

		req = urllib2.Request(self.INDUSTRY_LIST_URL)
		response = urllib2.urlopen(req)
	 	self.content = self.preprocess(response.read())
		response.close()

		return json.loads(self.content, encoding="gbk")
