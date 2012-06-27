#!/usr/bin/env python

import os
import sys
import urllib2
import time
import json
import re

from industry import industry_urls
from stock import stock_pull

def industry_pull(industry):
	# industry list
	start = time.time()

	req = urllib2.Request(industry_urls[industry])
	response = urllib2.urlopen(req)
	json_data = response.read()

	elapsed = time.time() - start
	print "pull industry list elapsed: ",
	print str(elapsed) + "s"

	# json_data = '[{symbol:"sh600048",code:"600048",name:"111",trade:"11.380",pricechange:"0.140",changepercent:"1.246",buy:"11.380",sell:"11.390",settlement:"11.240",open:"11.120",high:"11.460",low:"11.070",volume:"13996104",amount:"158807904",ticktime:"10:35:31",per:10.345,pb:1.89,mktcap:8123037.616958,nmc:7979513.746586,turnoverratio:0.19961}]'	

	# replace ticktime error data
	json_data = re.sub(r'\d+:\d+:\d+', '', json_data)
 
	# adjust JSON format
	json_data = re.sub(r"{\s*(\w)", r'{"\1', json_data)
	json_data = re.sub(r",\s*(\w)", r',"\1', json_data)
	json_data = re.sub(r"(\w):", r'\1":', json_data)

	industrys = json.loads(json_data, encoding="GB2312")

	print "total " + industry + ": "  + str(len(industrys))

	for industry in industrys:
		print industry["symbol"] + " " + industry["code"] + " " + industry["name"]
		stock_pull(industry["code"])
		break
