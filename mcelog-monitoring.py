#!/usr/bin/env python

import socket
import os
import sys
import shutil

path = ('/var/log/mcelog')
second_path = ('/local/tmp/mcelog-count.txt')
treshold = 100

hostname = socket.gethostname()

if os.path.exists(path) == False:
        exit()

ExcludeHosts = [ 'hostname1', 'hostname2', 'hostname3' ]

if hostname in ExcludeHosts:
        treshold = 100

step1 = sum(1 for l in open(path, 'r'))
step2 = sum(1 for l in open(second_path, 'r'))
step = step1 - step2

if step > treshold:
        print 1
else:
        print 0

shutil.copy(path, secondpath)
