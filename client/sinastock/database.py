#!/usr/bin/env python

import os
import sqlite3

from industry import *
from stock import *

class database():
	def __init__(self, home, name):
		self.conn = sqlite3.connect(home + '/' + name + '.db')

	def __del__(self):
		self.conn.close()

	def install(self):
		print 'database install'
		cur = self.conn.cursor()

		# industry
		sql = "create table if not exists industry( \
				id integer primary key autoincrement, \
				pid integer, \
				code varchar(64), \
				name varchar(128) UNIQUE)"
		cur.execute(sql);
		cur.execute('create unique index if not exists industry_code_index on industry(code)')
		cur.execute('create unique index if not exists industry_name_index on industry(name)')

		# stock
		sql = "create table if not exists stock( \
				id integer primary key autoincrement, \
				symbol char(12), \
				code char(12), \
				name varchar(32), \
				industry_id integer, \
				year integer "
 		for i in range(len(financial_keys)):
			sql += ' , data' + str(i) + ' float'

		sql += ', foreign key(industry_id) references industry(id))'
		cur.execute(sql)
		cur.execute('create unique index if not exists stock_symbol_index on stock(symbol)')
		cur.execute('create unique index if not exists stock_name_index on stock(name)')
		cur.close()

	def uninstall(self):
		print 'database uninstall'
		cur = self.conn.cursor()
		cur.execute('drop table if exists industry')
		cur.execute('drop table if exists stock')
		cur.close()

	def industry_add(self, ind):
		cur = self.conn.cursor()
		cur.executemany('insert into industry values(?, ?, ?)', ind.pid, ind.code, ind.name)
		cur.close()

	def industry_query(self, name):
		cur = self.conn.cursor()
		cur.execute('select * from industry where name=?', name)

		results = cur.fetchone()
		ind = industry()
		ind.id = results[0]
		ind.pid = results[1]
		ind.code = results[2]
		ind.name = name
	
		cur.close()
		return ind

	def stock_add(self, stock):
		cur = self.conn.cursor()
		sql = 'insert into stock values(%s, %s, %s, %d, %d, '%(stock.symbol, stock.code, stock.name, stock.industry_id, stock.year)
		values = stock.get_values()
		for i in range(len(financial_keys)):
			sql += values[financial_keys[i]] + ', '
		sql += ')'	
		cur.execute(sql)
		cur.close()
