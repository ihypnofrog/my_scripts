#!/local/python/bin/python
## NOC - 894
# Author: Anton Timofeev; a.timofeev@corp.badoo.com

import sys
import os
import time
import subprocess
import datetime
from os import path, access
import re


PATH='/local/tmp/wwwrun/logs/SCTest.result.log'


## lose file = 999 code
def FileExistCheck():
	
	if path.exists(PATH) == False: 
		return "999"
	else:
		return "0"
	
if FileExistCheck() > '0' :
	debug_message = 'FILE IS MISSING'
	print '999'
	exit()
else:
	debug_message = 'FILE EXISTS, OK'

if len(sys.argv) == 2 and sys.argv[1] == "-d":
	print debug_message

## old file = 1 code

def TimeModifyCheck():
	last_file_modify = os.path.getmtime(PATH)
	time_now = time.time()
	delta = time_now - last_file_modify
	return delta

if TimeModifyCheck() > 10800 :
	debug_message = 'FILE IS TOO OLD'
	print '1'

if len(sys.argv) == 2 and sys.argv[1] == "-d" and TimeModifyCheck() > 10800:
	print debug_message
	exit()

if TimeModifyCheck() < 10800 :
	debug_message = 'FILE IS NOT OLD'

if len(sys.argv) == 2 and sys.argv[1] == "-d" :
	print debug_message

## LAST LINE PARSE 0 = OK; 2 = FAIL; 3 = UNKNOWN ERROR
def LastLineOK():
	test_ok = 'OK'
	last_line = subprocess.check_output(['tail', '-1', PATH])
	found = re.findall(test_ok, last_line)
	len(found) == last_line.count('OK')
	return len(found)

if LastLineOK() > 0:
	debug_message = 'LAST TEST IS OK, ALL IS OK'
	print '0'

if LastLineOK() > 0 and  len(sys.argv) == 2 and sys.argv[1] == "-d":
	print debug_message
	exit()


def LastLineFAIL():
	test_fail = 'FAIL'
	last_line = subprocess.check_output(['tail', '-1', PATH])
	found = re.findall(test_fail, last_line)
	len(found) == last_line.count('OK')
	return len(found)

if LastLineFAIL() > 0:
	debug_message = 'LAST TEST IS FAILED'
	print '2'

if LastLineFAIL() > 0 and  len(sys.argv) == 2 and sys.argv[1] == "-d":
	print debug_message
	exit()

def LastLineUNKNOWN():
	unknown = LastLineFAIL() + LastLineOK()
	return unknown

if LastLineUNKNOWN() == 0 and TimeModifyCheck() < 10800:
	debug_message = 'UNKNOWN ERROR, PLEASE CHECK FILE IN PATH'
	print '3'

if LastLineUNKNOWN() == 0 and len(sys.argv) == 2 and sys.argv[1] == "-d":
	print debug_message

