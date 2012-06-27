#!/usr/bin/env python

import os
import sys

from sinastock.robot import *

def main(argv):
	if len(argv) > 1:
		industry_pull(argv[1])
	else:
		print("Please type the short name of a Sina Stock Industry, for example 'fdc'.")

if __name__ == '__main__':
	main(sys.argv)
