#!/usr/bin/env python
#coding:gbk

import os
import sys
import urllib2

stock_financial_gl_urls = {
	"head":"http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/",
	"tail":"/ctrl/2011/displaytype/4.phtml",
}

class financial_parser():
	datas = ['总资产利润率(%)', '摊薄每股收益(元)']

	def parse(self, html):
		print html		

def stock_pull(id):
	url = stock_financial_gl_urls["head"] + id + stock_financial_gl_urls["tail"]

	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	html_data = response.read()

	parser = financial_parser()
	parser.parse(html_data)