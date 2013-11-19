#!/usr/bin/env python

import socket
import os
import sys
import shutil
import subprocess


# wwwstaff1.ulan - old server, this is Sun Fire X4100 M2


path = ('/var/log/mcelog')
second_path = ('/local/tmp/mcelog.log')
treshold = 100
hostname = socket.gethostbyaddr(socket.gethostname())[0]

if os.path.exists(second_path) == False:
	subprocess.call(['touch', second_path])

if os.path.exists(path) == False and len(sys.argv) == 2 and  sys.argv[1] == "-d" :
        print 'Error: file /var/log/mcelog is not found'
	exit()

if os.path.exists(path) == False:
        print 0
        exit()

ExcludeHosts = [ 'wwwstaff1.ulan', 'host2', 'host3' ] # if you add  new host, please anyway add comment
if hostname in ExcludeHosts:
	treshold = 1000

mcelog_lines_count_path1 = sum(1 for l in open(path, 'r'))
mcelog_lines_count_second_path = sum(1 for l in open(second_path, 'r'))
delta = mcelog_lines_count_path1 - mcelog_lines_count_second_path

if delta > treshold:
	output = 1
	debug = 'too many errors in mcelog'
else:
	output = 0
	debug = 'all is ok'

## truncate if mcelog has truncated

if delta < 0:
	debug = 'delta < 0. truncating file in second_path'
	target = open(second_path, 'w')
	target.truncate

if len(sys.argv) == 2 and sys.argv[1] == "-d" :
        print debug
else:
        print output

shutil.copy(path, second_path)
