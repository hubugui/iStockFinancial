#!/usr/bin/env python

import os
import sys

from sinastock.robot import *

def main(argv):
	if len(argv) > 2:
		rbt = robot(argv[1], argv[2])
		rbt.go()
	else:
		print("for example: 'python main.py 2011 /opt/istock'")

if __name__ == '__main__':
	import stacktracer
	stacktracer.trace_start("trace.html",interval=5,auto=True)

	main(sys.argv)
