#!/usr/bin/env python

import os
import sys
import time
import urllib2
import urllib3
import socket

from urllib3 import *

urls = \
[
	'/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&node=hangye_ZA01',
	'/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&node=hangye_ZA03',
	'/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&node=hangye_ZA05',
	'/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&node=hangye_ZA07',
	'/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&node=hangye_ZA09',
	'/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&node=hangye_ZB01',
	'/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&node=hangye_ZB03',
	'/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&node=hangye_ZB05',
	'/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&node=hangye_ZB07',
	'/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&node=hangye_ZB49',
]

def urllib2_pull():
	for url in urls:
		response = urllib2.urlopen(urllib2.Request(url))
		content = response.read()
		response.close()

		print '.',
	print ''

def urllib3_pull():

	ip = socket.gethostbyname(socket.gethostname())
	if ip.startswith('137.'):
		http_pool = urllib3.HTTPConnectionPool('10.77.8.70:8080', maxsize = 10)
	else:
		http_pool = urllib3.HTTPConnectionPool('vip.stock.finance.sina.com.cn', maxsize = 10)

	for url in urls:
		if ip.startswith('137.'):
			url = 'http://vip.stock.finance.sina.com.cn' + url
		r = http_pool.urlopen('GET', url, assert_same_host=False)
		print len(r.data)
	print ''

def urllib3_pool_pull():
	http = urllib3.PoolManager()
	r = http.request('GET', 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=10000&sort=symbol&asc=1&node=hangye_ZA01&_s_r_a=auto')
	print r.status, r.data

def main(argv):
	begin = time.time()

	#urllib2_pull()

	end = time.time()
	print 'urllib2> elapsed time %ds'%(end - begin)

	begin = time.time()

	#urllib3_pull()
	urllib3_pool_pull()

	end = time.time()
	print 'urllib3> elapsed time %ds'%(end - begin)

if __name__ == '__main__':
	main(sys.argv)
