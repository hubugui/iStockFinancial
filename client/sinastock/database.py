#!/usr/bin/env python

import os
import sqlite3

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
				name varchar(128) UNIQUE)"
		cur.execute(sql);
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

		sql += ', foreign key(industry_id) references industry(id)'
		sql += ')'
		cur.execute(sql)
		cur.execute('create unique index if not exists stock_name_index on stock(name)')

		cur.close()

	def uninstall(self):
		print 'database uninstall'

		cur = self.conn.cursor()
		cur.execute('drop table if exists industry')
		cur.execute('drop table if exists stock')
		cur.close()

	def industry_add(self, industry):
		cur = self.conn.cursor()
		cur.executemany('insert into industry values(?, ?)', industry.pid, industry.name)
		cur.close()

	def industry_query(self, name):
		cur = self.conn.cursor()
		cur.execute('select * from industry where name=?', name)
		results = cur.fetchone()

		ind = industry()
		ind.id = results[0]
		ind.pid = results[0]
		ind.name = name
		
		cur.close()

	def stock_add(self, stock):
		cur = self.conn.cursor()

		sql = 'insert into stock values(?, ?)'
		cur.execute(sql)
		cur.close()
