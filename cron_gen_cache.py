#! /usr/bin/env python

# Automatically fetch info from hospitals everyday.


import os, sys

SERVER_ROOT = '/srv/www/'
lmr_path_list = [
    'chyi/'
]
cache_gen_file = 'cache.py'
for hos in lmr_path_list:
    if os.fork():   
        continue
    os.chdir(SERVER_ROOT + hos)
    os.system('./' + cache_gen_file)
    os.system('chown www-data:www-data *.pickle')
exit(0)


