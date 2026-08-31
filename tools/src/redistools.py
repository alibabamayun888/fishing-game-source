#!/usr/bin/env python 
# -*- coding=utf-8 -*-
# author: CongSheng Peng
# Create time: 2018-04-17

import sys
import msgpack
import redis
import traceback
import json
reload(sys)
sys.setdefaultencoding('utf8')

len(sys.argv)

connHost = ""
connPort = 0
keyName  = ""
authCode = ""
hgetKey = 0

connHost = str(sys.argv[1])
connPort = int(sys.argv[2])
keyName  = str(sys.argv[3])

if len(sys.argv) == 5:
	hgetKey = int(sys.argv[4])

if len(sys.argv) == 6:
	authCode = str(sys.argv[5])


def printDict(printBuffer):
	printStr = ""
	for key, value in printBuffer.items():
		printStr += "{" + str(key) + ":"
		if (type(value).__name__ == "dict") and value:
			printStr += printDict(value)
		else:
			printStr += str(value)+"}"
	return printStr


try:
	redisConn = redis.Redis(host = connHost, port = connPort, db = 0, password = authCode)
	if redisConn:
		keyDict = {}
		if hgetKey > 0:
			keyDict = redisConn.hget(keyName, hgetKey)
		else:
			keyDict = redisConn.hgetall(keyName)
		if keyDict:
			if hgetKey <= 0:
				for key, value in keyDict.items():
					print "key:%s" % str(key)
					decodeMsg = msgpack.unpackb(value)
					if type(decodeMsg).__name__ == "dict":
						json_string=json.dumps(decodeMsg)
						print json_string.encode("utf-8")
					else:
						print value
					print "+++++" * 20
			else:
				decodeMsg = msgpack.unpackb(keyDict)
				print decodeMsg
		else:
			print "hgetall buffer is empty!"
	else:
		print "redis connection error"
except:
	traceback.print_exc()
