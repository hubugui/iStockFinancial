#!/usr/bin/env python

import os
import sys
import urllib2
from sgmllib import SGMLParser

class job():
	idx = 1

	def __init__(self, name, url, onsuccess, onfailure, userdata):
		self.name = name
		self.url = url
		self.onsuccess = onsuccess
		self.onfailure = onfailure
		self.userdata = userdata