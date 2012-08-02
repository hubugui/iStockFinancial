#!/usr/bin/env python

import sys
import time

from sinastock.crawler import *
from sinastock.robot import *
from sinastock.setting import *

def usage():
	print "for example: 'python main.py /opt/istock 2011'"
	print "for example: 'python main.py .', This means that pull data of from year 1989 to the system time"

def main(argv):
	setting['crawler'] = crawler(10, 5, 500)
	setting['robot'] = robot()

	if len(argv) == 3:
		# Normal, this case as increment pull or test 
		setting['home'] = argv[1]
		setting['years'] = [int(argv[2])]
		setting['robot'].go()
	elif len(argv) == 2:
		# pull all data since year 1989
		years = []
		system_year = time.gmtime()[0]
		for year in range(1989, system_year):
			years.append(year)

		setting['home'] = argv[1]
		setting['years'] = years
		if len(years) > 0:
			setting['robot'].go()
		else:
			print 'error in your system time less than year 1989'
			usage()
	else:
		usage()

if __name__ == '__main__':
	try:
		main(sys.argv)
	except:
		s = sys.exc_info()
		print "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)
        usage()		
