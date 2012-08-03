#!/usr/bin/env python
#coding:gbk

from sgmllib import SGMLParser

key_separator = '^_^'
years_key = '��������'
financial_keys = \
[
	'���ʲ�������(%)',
	'��Ӫҵ��������(%)',
	'���ʲ���������(%)',
	'�ɱ�����������(%)',
	'Ӫҵ������(%)',
	'��Ӫҵ��ɱ���(%)',
	'���۾�����(%)',
	'�ɱ�������(%)',
	'���ʲ�������(%)',
	'�ʲ�������(%)',
	'����ë����(%)',
	'������ñ���',
	'����Ӫ����',			
	'��Ӫ�������',
	'��Ϣ������(%)',
	'Ͷ��������(%)',
	'��Ӫҵ������(Ԫ)',
	'���ʲ�������(%)',
	'��Ȩ���ʲ�������(%)',
	'�۳��Ǿ����������ľ�����(Ԫ)',
	'��Ӫҵ������������(%)',
	'������������(%)',
	'���ʲ�������(%)',
	'���ʲ�������(%)',
	'Ӧ���˿���ת��(��)',
	'Ӧ���˿���ת����(��)',
	'�����ת����(��)',
	'�����ת��(��)',
	'�̶��ʲ���ת��(��)',
	'���ʲ���ת��(��)',
	'���ʲ���ת����(��)',
	'�����ʲ���ת��(��)',
	'�����ʲ���ת����(��)',
	'�ɶ�Ȩ����ת��(��)',
	'��������',
	'�ٶ�����',
	'�ֽ����(%)',			
	'��Ϣ֧������',
	'����ծ����Ӫ���ʽ����(%)',
	'�ɶ�Ȩ�����(%)',			
	'���ڸ�ծ����(%)',
	'�ɶ�Ȩ����̶��ʲ�����(%)',
	'��ծ��������Ȩ�����(%)',			
	'�����ʲ��볤���ʽ����(%)',
	'�ʱ�������(%)',
	'�̶��ʲ���ֵ��(%)',
	'�ʱ��̶�������(%)',
	'��Ȩ����(%)',
	'�����ֵ����(%)',			
	'�̶��ʲ�����(%)',
	'�ʲ���ծ��(%)',
	'���ʲ�(Ԫ)',
	'��Ӫ�ֽ������������������(%)',
	'�ʲ��ľ�Ӫ�ֽ������ر���(%)',
	'��Ӫ�ֽ������뾻����ı���(%)',			
	'��Ӫ�ֽ������Ը�ծ����(%)',
	'�ֽ���������(%)',
]

class stock_parser(SGMLParser):
	td_segment=False
	a_segment=False
	intercept=False
	data_idx=1
	key=''
	
	years_intercept = False

	def reset(self):
		self.urls=[]
		SGMLParser.reset(self)

	def parse(self, data, values, years):
		self.values = values
		self.years = years
		self.feed(data)
		self.close()

	def start_td(self, attr):
		self.td_segment = True

	def end_td(self):
		self.td_segment = False
		self.years_intercept = False

	def start_a(self, attrs):
		self.a_segment = True

	def end_a(self):
		self.a_segment = False

	def handle_financial(self, data):
		if self.a_segment == True:
			if data in financial_keys:
				self.intercept = True
				#self.key = str('%3d'%(self.data_idx)) +  key_separator + data
				self.key = data
				self.data_idx += 1
		elif self.td_segment == True:
			if self.intercept == True:
				if len(data) > 0:
					self.intercept = False

					try:
						value = float(data)
					except:
						value = float(0.0)

					if self.key not in self.values:
						self.values[self.key] = value

					#print self.key + ":" + str(self.values[self.key])
					#print '.',

	def handle_years(self, data):
		if self.a_segment == True:
			if self.years_intercept == True:
				if len(data) > 0:
					self.years.append(data)
		elif self.td_segment == True:
			if data.startswith(years_key):
				self.years_intercept = True

	def handle_data(self, data):
		data = data.strip(' \t\n\r')
		self.handle_financial(data)
		self.handle_years(data)
