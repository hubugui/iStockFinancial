#!/usr/bin/env python

import os
import sys
import urllib2
from sgmllib import SGMLParser

class job():
	idx = 1
	name = ''
	url = ''
	year = 2011

	def __init__(self, name, url, onsuccess, onfailure, userdata):
		self.name = name
		self.url = url
		self.onsuccess = onsuccess
		self.onfailure = onfailure
		self.userdata = userdata

	def set_idx(self, idx):
		self.idx = idx

	def get_idx(self):
		return self.idx

	def set_year(self, year):
		self.year = year

	def get_year(self):
		return self.year

	def onsuccess(self, content):
		return None

	def onfailure(self, content):
		return None
