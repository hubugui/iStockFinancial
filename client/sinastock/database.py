#!/usr/bin/env python

import os
import sqlite3
import sys
import time
import threading

sys.path.append('././')

from common.util import *
from industry import *
from stock import *

class database():	
	def __init__(self, home, name):
		self.path = home + '/' + name + '-' + get_time(time.time()) + '.db'
		self.pools = {}

	def connect(self):
		#print threading.currentThread().getName()
		if threading.currentThread().getName() not in self.pools:
			conn = sqlite3.connect(self.path)
			self.pools[threading.currentThread().getName()] = conn
		else:
			conn = self.pools[threading.currentThread().getName()]
		return conn

	def disconnect(self, conn):
		if threading.currentThread().getName() not in self.pools:
			conn = sqlite3.connect(self.path)
			self.pools[threading.currentThread().getName()] = conn
		else:
			conn = self.pools[threading.currentThread().getName()]
		conn.close()

	def install(self):
		print 'database install'
		cur = self.connect().cursor()

		# industry
		sql = "create table if not exists industry( \
			id integer primary key autoincrement, \
			name varchar(128), \
			code varchar(64), \
			pid integer)"
		cur.execute(sql);
		cur.execute('create unique index if not exists industry_name_code_index on industry(name, code)')

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
		cur.execute('create unique index if not exists stock_symbol_index on stock(symbol, year)')
		cur.execute('create unique index if not exists stock_name_index on stock(name, year)')
		cur.close()

	def uninstall(self):
		print 'database uninstall'
		cur = self.connect().cursor()
		cur.execute('drop table if exists industry')
		cur.execute('drop table if exists stock')
		cur.close()

	def industry_add(self, ind):
		conn = self.connect()
		cur = conn.cursor()
		cur.execute("insert into industry values(null, '%s', '%s', '%d')"%(ind.name, ind.code, ind.pid))
		conn.commit()
		cur.close()
		return cur.lastrowid

	def industry_query(self, name):
		conn = self.connect()
		cur = conn.cursor()
		cur.execute("select * from industry where name='%s'"%(name))

		results = cur.fetchone()
		ind = industry()
		ind.id = results[0]
		ind.name = results[1]
		ind.code = results[2]
		ind.pid = results[3]

		cur.close()
		return ind

	def stock_add(self, stock):
		values = stock.get_values()
		conn = self.connect()
		cur = conn.cursor()
		sql = "insert into stock values(null, '%s', '%s', '%s', %d, %d"%(stock.symbol, stock.code, stock.name, stock.industry_id, stock.year)
		for i in range(len(financial_keys)):
			sql += ', ' + str(values[financial_keys[i]])
		sql += ')'

		#print sql
		
		cur.execute(sql)
		conn.commit()
		cur.close()
		return cur.lastrowid
