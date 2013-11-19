#!/usr/bin/env python
#NOC-879
#Author: Anton Timofeev

import subprocess
import pprint
import sys

def func1():

        check = subprocess.Popen(["/local/php5/bin/php", "/local/www/_scripts/run.php", "\\ScriptFramework\\Script_Monitoring"], stdout=subprocess.PIPE)
        check1=check.stdout.read().strip()
        sum_index=check1.index('[')
        return check1[:sum_index]

def duplicates(l):
        temp = []
        dupl = []
        for x in l:
                if x in temp:
                        dupl.append(x)
                else:
                        temp.append(x)
        return dupl.sort()

def main():

        if len(sys.argv) == 2 and sys.argv[1] == "-d":
                print "debug mode"
                debug = True
        else:
                debug = False

        first_res = func1().split('\n')
        second_res = func1().split('\n')

        dup1 = duplicates(first_res)
        dup2 = duplicates(second_res)
        if debug:
                pprint.pprint(dup1)
                pprint.pprint(dup2)

        if dup1 == dup2 and dup1 != None:
                print "problem, these are duplicates", dup1
        else:
                print "OK"


main()
