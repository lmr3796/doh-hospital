#! /usr/bin/env python

# Automatically fetch info from hospitals everyday.

LOCAL_SERVER_ROOT = '/srv/www/doh'
import os, sys
import lmr3796
path_list = [
	'/chcg',
	'/chyi',
	'/hwln',
	'/mil',
	'/syh',
	'/taic',
	'/tnh',
	'/tygh',
]
os.system("find . -name *.pickle|xargs /bin/rm -f")
if os.fork() == 0:
	for hos in path_list:
		if os.fork() == 0:
			running = LOCAL_SERVER_ROOT + hos
	   		os.chdir(running)
			lmr3796.set_path(running + '/doh.json')
			lmr3796.get_all_dept('true')
			lmr3796.get_all_doc('true')
			os.system('chown www-data:www-data *.pickle')
	exit(0)
exit(0)


