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
	content = ''
	finish = False

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

	def get_url(self):
		return self.url

	def set_content(self, content):
		self.content = content

	def get_content(self):
		return self.content

	def onsuccess(self):	
		return None

	def onfailure(self, content):
		return None
