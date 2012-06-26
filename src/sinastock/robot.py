#!/usr/bin/env python

import os
import sys
import urllib2

from industry import *

def fetch(industry):
	req = urllib2.Request(industry_urls[industry])
	response = urllib2.urlopen(req)
	the_page = response.read()

	print(the_page)
