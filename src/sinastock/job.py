#!/usr/bin/env python

import os
import sys
import urllib2
from sgmllib import SGMLParser

class job():
	idx = 1
	name = ''
	queue = None

	def __init__(self, name, url, onsuccess, onfailure, userdata):
		self.name = name
		self.url = url
		self.onsuccess = onsuccess
		self.onfailure = onfailure
		self.userdata = userdata

	def set_idx(self, idx):
		self.idx = idx

	def set_queue(self, queue):
		self.queue = queue

	def get_queue(self):
		return self.queue

	def onsuccess(self, content):
		return None

	def onfailure(self, content):
		return None
