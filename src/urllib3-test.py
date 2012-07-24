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
	'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&node=hangye_ZA01',
	'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&node=hangye_ZA03',
	'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&node=hangye_ZA05',
	'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&node=hangye_ZA07',
	'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&node=hangye_ZA09',
	'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&node=hangye_ZB01',
	'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&node=hangye_ZB03',
	'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&node=hangye_ZB05',
	'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&node=hangye_ZB07',
	'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&node=hangye_ZB49',
	'http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/900930/ctrl/2011/displaytype/4.phtml',
	'http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/900931/ctrl/2011/displaytype/4.phtml',
	'http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/900932/ctrl/2011/displaytype/4.phtml',
	'http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/900933/ctrl/2011/displaytype/4.phtml',
	'http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/900934/ctrl/2011/displaytype/4.phtml',
	'http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/900935/ctrl/2011/displaytype/4.phtml',
	'http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/900936/ctrl/2011/displaytype/4.phtml',
	'http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/900937/ctrl/2011/displaytype/4.phtml',
	'http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/900938/ctrl/2011/displaytype/4.phtml',
	'http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/900939/ctrl/2011/displaytype/4.phtml',
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
		http_pool = HTTPConnectionPool('10.77.8.70:8080', maxsize = 10)
	else:
		http_pool = HTTPConnectionPool('vip.stock.finance.sina.com.cn', maxsize = 10)

	for url in urls:
		r = http_pool.urlopen('GET', url, assert_same_host=False)
		print '.',
	print ''

def main(argv):
	begin = time.time()

	urllib2_pull()

	end = time.time()
	print 'urllib2> elapsed time %ds'%(end - begin)

	begin = time.time()

	urllib3_pull()

	end = time.time()
	print 'urllib3> elapsed time %ds'%(end - begin)

if __name__ == '__main__':
	main(sys.argv)
