#!/usr/bin/env python

import os
import sys

from industry import *

def robot_go(argv):
	if len(argv) > 3:
		industry_pull(argv[1], argv[2], argv[3])
	else:
		print("for example: 'python main.py fdc 2011 10'")
		print("for example: 'python main.py jrhy 2010 100'")
