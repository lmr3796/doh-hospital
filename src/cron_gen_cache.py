#! /usr/bin/env python
# coding=utf-8

# Automatically fetch info from hospitals everyday.

import os, sys
import lmr3796
from datetime import date
LOCAL_SERVER_ROOT = '/srv/www/doh'
hos_list = [hos for hos in os.listdir(LOCAL_SERVER_ROOT) if os.path.isdir(hos)]
def make_cache(hos):
    os.chdir(hos)
    print >> sys.stderr, r'[' + hos + r']'
    lmr3796.set_env('doh.json')
    lmr3796.get_all_dept(True)
    lmr3796.get_all_doc(True)
    os.system('chown www-data:lmr3796 *.pickle')
    os.system('chmod 664 *.pickle')
    print >> sys.stderr, ''
    os.chdir('..')

def main():
    os.chdir(LOCAL_SERVER_ROOT)
    if len(sys.argv) > 1:
        make_cache(sys.argv[1])
    else:
        fail_list = []
        print >> sys.stderr, 'Clear all cache files.'
        os.system("find . -name *.pickle|xargs /bin/rm -f")
        for hos in hos_list:
            try:
                make_cache(hos)
            except BaseException as e:
                fail_list.append((hos,e))
        if not fail_list:
            errlog = open('cron_gen_cache.log','a')
            for hos, e in fail_list:
                print >> errlog, r'['+hos+r']'
                print >> errlog, date.today()
                print >> errlog, e
                print >> errlog, ''
            errlog.close()
            return 1
        else:
            print >> sys.stderr, 'All hospitals done!'

    return 0

if __name__ == '__main__':
    exit(main())


