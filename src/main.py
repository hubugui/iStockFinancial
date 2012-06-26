#!/usr/bin/env python

import os
import sys

from sinastock.robot import *

def main(argv):
	fetch(argv[1])

if __name__ == '__main__':
	main(sys.argv)
