#!/usr/bin/env python
#coding:gbk

import os
import sys
import urllib2
from sgmllib import SGMLParser

key_separator = '^_^'
financial_keys = \
[
	'总资产利润率(%)',
	'主营业务利润率(%)',
	'总资产净利润率(%)',
	'成本费用利润率(%)',
	'营业利润率(%)',
	'主营业务成本率(%)',
	'销售净利率(%)',
	'股本报酬率(%)',
	'净资产报酬率(%)',
	'资产报酬率(%)',
	'销售毛利率(%)',
	'三项费用比重',
	'非主营比重',			
	'主营利润比重',
	'股息发放率(%)',
	'投资收益率(%)',
	'主营业务利润(元)',
	'净资产收益率(%)',
	'加权净资产收益率(%)',
	'扣除非经常性损益后的净利润(元)',
	'主营业务收入增长率(%)',
	'净利润增长率(%)',
	'净资产增长率(%)',
	'总资产增长率(%)',
	'应收账款周转率(次)',
	'应收账款周转天数(天)',
	'存货周转天数(天)',
	'存货周转率(次)',
	'固定资产周转率(次)',
	'总资产周转率(次)',
	'总资产周转天数(天)',
	'流动资产周转率(次)',
	'流动资产周转天数(天)',
	'股东权益周转率(次)',
	'流动比率',
	'速动比率',
	'现金比率(%)',			
	'利息支付倍数',
	'长期债务与营运资金比率(%)',
	'股东权益比率(%)',			
	'长期负债比率(%)',
	'股东权益与固定资产比率(%)',
	'负债与所有者权益比率(%)',			
	'长期资产与长期资金比率(%)',
	'资本化比率(%)',
	'固定资产净值率(%)',
	'资本固定化比率(%)',
	'产权比率(%)',
	'清算价值比率(%)',			
	'固定资产比重(%)',
	'资产负债率(%)',
	'总资产(元)',
	'经营现金净流量对销售收入比率(%)',
	'资产的经营现金流量回报率(%)',
	'经营现金净流量与净利润的比率(%)',			
	'经营现金净流量对负债比率(%)',
	'现金流量比率(%)',
]

class stock_parser(SGMLParser):
	key = ''
	td_segment = False
	a_segment = False
	intercept = False
	data_idx = 1

	def reset(self):
		self.urls=[]
		SGMLParser.reset(self)

	def parse(self, data, values):
		self.values = values
		self.feed(data)
		self.close()

	def start_td(self, attr):
		self.td_segment = True

	def end_td(self):
		self.td_segment = False

	def start_a(self, attrs):
		self.a_segment = True

	def end_a(self):
		self.a_segment = False

	def handle_data(self, data):
		if self.a_segment == True:
			if data in financial_keys:
				self.intercept = True
				self.key = str('%3d'%(self.data_idx)) +  key_separator + data
				self.data_idx += 1
		elif self.td_segment == True:
			if self.intercept == True:
				data = data.strip(' \t\n\r')
				if len(data) > 0:
					self.intercept = False

					try:
						value = float(data)
					except:
						value = float(0.0)

					if self.key in self.values:
						self.values[self.key] = self.values[self.key] + value
					else:
						self.values[self.key] = value

					# print self.key + ":" + str(self.values[self.key])
					# print '.',
