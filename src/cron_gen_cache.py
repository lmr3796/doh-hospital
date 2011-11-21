#! /usr/bin/env python

# Automatically fetch info from hospitals everyday.

LOCAL_SERVER_ROOT = '/srv/www/doh'
#LOCAL_SERVER_ROOT = '/home/lmr3796/hospital/deploy'
import os, sys
import lmr3796
hos_list = [
	'/chcg',
	'/chyi',
	'/mil',
	'/syh',
	'/taic',
	'/tnh',
	'/tygh',
]

def make_cache(hos):
	running = LOCAL_SERVER_ROOT + hos
	os.chdir(running)
	lmr3796.set_env(running + '/doh.json')
	lmr3796.get_all_dept(True)
	lmr3796.get_all_doc(True)
    os.system('chown www-data:lmr3796 *.pickle')
    os.system('chmod 664 *.pickle')

def main():
	print >> sys.stderr, 'Clear all cache files.'
	os.system("find . -name *.pickle|xargs /bin/rm -f")
	if len(sys.argv) > 1:
		make_cache(sys.argv[1])
	else:
		for hos in hos_list:
			print >> sys.stderr, r'[' + hos[1:] + r']'
			make_cache(hos)
			print >> sys.stderr, ''
	print >> sys.stderr, 'All hospitals done!'
	return 0

if __name__ == '__main__':
	exit(main())


