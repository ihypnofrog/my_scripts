#!/bin/bash
#  Author: Anton Timofeev
#  https://jira.badoojira.com/browse/NOC-875


host_name=$(echo $(facter hostname 2>/dev/null).$(facter domain 2>/dev/null))
mm_name=`dig txt +short $host_name | sed -e 's/"//g;s/\;.*//g;s/^$//g;s/\ /\n/g'`
lan_count=`facter domain`
mlan='mlan'

if [ "$lan_count" = "$mlan" ]
	then
	d='4'
		else 
	d='2'
fi

if [ "$lan_count" = "$mlan" ]
	then
	platform='1'
		else
	platform='2'
fi

if [ "$d" = "4" ]
	then
	lan='mlan'
		else
	lan='ulan'
fi

for i in `dig txt +short $host_name | sed -e 's/"//g;s/\;.*//g;s/^$//g;s/\ /\n/g'`;
do wget -q "http://rrd$d.$lan/api.php?var_dump=1&method=get_metrics_values&unit=MeetMakerStat&metric[]=$platform/$i.$lan/ru_stime&limit=1" -O /local/tmp/$i; done

for i in `dig txt +short $host_name | sed -e 's/"//g;s/\;.*//g;s/^$//g;s/\ /\n/g'`;
do wget -q "http://rrd$d.$lan/api.php?var_dump=1&method=get_metrics_values&unit=MeetMakerStat&metric[]=$platform/$i.$lan/ru_utime&limit=1" -O /local/tmp/s$i; done

for i in `ls /local/tmp/meetmaker-*`; do cat $i | grep \\[value\\] |  sed  's/\[value\] =>//g' | sed 's/^[ \t]*//' |  awk -F '.' '{if ($2>0) print ($2); else print ("0");}' | cut -c-2; done > /local/tmp/meetmakers_rusage_rtime.txt

for i in `ls /local/tmp/smeetmaker-*`; do cat $i | grep \\[value\\] |  sed  's/\[value\] =>//g' | sed 's/^[ \t]*//' |  awk -F '.' '{if ($2>0) print ($2); else print ("0");}' | cut -c-2; done > /local/tmp/meetmaker_rusage_stime.txt
paste /local/tmp/meetmakers_rusage_rtime.txt /local/tmp/meetmaker_rusage_stime.txt -d + | bc > /local/tmp/meetmakers_all_rusage.txt
cat /local/tmp/meetmakers_all_rusage.txt | sort -nr | head -1

