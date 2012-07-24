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
	'/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&node=hangye_ZB50',
	'/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&node=hangye_ZC0',
	'/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&node=hangye_ZC1',
]

def urllib2_pull():
	for url in urls:
		url = 'http://vip.stock.finance.sina.com.cn/' + url
		response = urllib2.urlopen(urllib2.Request(url))
		content = response.read()
		response.close()

		print '.',
	print ''

def urllib3_pull():
	ip = socket.gethostbyname(socket.gethostname())
	if ip.startswith('137.'):
		http_pool = HTTPConnectionPool('10.77.8.70:8080', maxsize = 10)
	else:
		http_pool = HTTPConnectionPool('vip.stock.finance.sina.com.cn', maxsize = 10)

	for url in urls:
		url = 'http://vip.stock.finance.sina.com.cn/' + url	
		r = http_pool.urlopen('GET', url, assert_same_host=False)
		print '.',
	print ''

def main(argv):
	begin = time.time()

	urllib2_pull()

	end = time.time()
	print 'urllib2_pull> elapsed time %ds'%(end - begin)

	begin = time.time()

	urllib3_pull()

	end = time.time()
	print 'urllib3_pull> elapsed time %ds'%(end - begin)

if __name__ == '__main__':
	main(sys.argv)
