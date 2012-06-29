#!/usr/bin/env python
#coding:gbk

import os
import sys
import urllib2
import time
import json
import re
import xlwt

from stock import key_separator
from stock import stock_pull
from stock import stock_url

def write_console(values, count):
	for key, value in sorted(values.iteritems()):
		key_pack = key.split(key_separator)

		print key_pack[0] + "." + key_pack[1] + ":" + str(value / count)

def write_excel(values, count, path):
	wbk = xlwt.Workbook()
	sheet = wbk.add_sheet('sheet 1', cell_overwrite_ok=True)

	# head style
	head_style = xlwt.XFStyle()

	# font
	head_font = xlwt.Font()
	head_font.colour_index = 4
	head_font.width = 256 * 100
	head_font.height = 8*20

	head_style.font = head_font

	# alignment
	head_alignment = xlwt.Formatting.Alignment()
	head_alignment.horz = xlwt.Formatting.Alignment.HORZ_CENTER
	head_alignment.vert = xlwt.Formatting.Alignment.VERT_CENTER

	head_style.alignment = head_alignment

	sheet.write(0, 0, '名称'.decode('gbk'), head_style)
	sheet.write(0, 1, '数值'.decode('gbk'), head_style)

	# col width
	sheet.col(0).width = 256 * 40
	sheet.col(1).width = 256 * 40

	for key, value in sorted(values.iteritems()):
		key_pack = key.split(key_separator)

		row = int(key_pack[0]) + 1
		sheet.write(row, 0, key_pack[1].decode('gbk'))
		sheet.write(row, 1, value / float(count))

	wbk.save(path)

def industry_pull(name, year, count):
	count = int(count)

	# url
	url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&asc=1&node=new_%s&_s_r_a=setlen'%(name)
	print "pull: " + url

	# http
	start = time.time()

	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	json_data = response.read()

	elapsed = time.time() - start
	print "pull elapsed: ",
	print str(elapsed) + "s"

	# replace ticktime error data
	json_data = re.sub(r'\d+:\d+:\d+', '', json_data)

 	# adjust json format
	json_data = re.sub(r"{\s*(\w)", r'{"\1', json_data)
	json_data = re.sub(r",\s*(\w)", r',"\1', json_data)
	json_data = re.sub(r"(\w):", r'\1":', json_data)
	# json
	stocks = json.loads(json_data, encoding="gbk")
	print "total " + name + " corp number: "  + str(len(stocks))

	# stock foreach
	values = {}
	idx = 0
	for stock in stocks:
		idx += 1
		if idx > count:
			break

		print "--------------------------------------------------"
		print str(idx) + "\t" + stock["symbol"] + "\t" + stock["code"] + "\t\t" + stock["name"]
		print stock_url(stock["code"], year)
		print "--------------------------------------------------"

		stock_pull(stock["code"], year, values)

	write_console(values, count)
	write_excel(values, count, "%s_%s_%s.xls"%(name, year, count))
