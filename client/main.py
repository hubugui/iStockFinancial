#!/usr/bin/env python

import os
import sys

from sinastock.robot import *
from sinastock.crawler import *

def main(argv):
	craw = crawler(10, 5, 500)
	if len(argv) == 3:
		rbt = robot(argv[1], argv[2], craw)
		rbt.go()
	elif len(argv) == 2:
		elapsed = 0
		for year in range(1989, 2012):
			rbt = robot(argv[1], str(year), craw)
			elapsed += rbt.go()

		print 'total elapsed %ds'%(elapsed)
	else:
		print("for example: 'python main.py /opt/istock 2011'")
		print("for example: 'python main.py .'")

if __name__ == '__main__':
	main(sys.argv)
