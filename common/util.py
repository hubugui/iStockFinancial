#!/usr/bin/env python

import os
import sys

def file_exist(path):
	if os.path.isdir(path):
		return os.path.exists(path)
	else:
		return os.path.isfile(path)

def file_size(path):
	if os.path.isfile(path):
		return os.stat(path).st_size
	else:
		return 0
