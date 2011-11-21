#! /usr/bin/env python
# coding=utf-8
import json,os,sys
import lmr3796
from BeautifulSoup import BeautifulSoup
NAME        =    u'王小明'
IDEN        =    'E123867366'
BIRTH       =    '1991-01-01'
ORIGIN      =    '1'
FIRST       =    '1'
MARRIAGE    =    '1'
GENDER      =    '1'

HOS_NAME    =[
                #'mil',
                #'chcg',
                #'chyi',
                #'syh',
                #'tnh',
                #'tygh',
                'taic'
            ]
def status_dump(hos, dept_id, doc_id, time, status):
    print >> sys.stderr, hos
    print >> sys.stderr, dept_id 
    print >> sys.stderr, doc_id
    print >> sys.stderr, time
    if status is not None:
        for k,v in status.iteritems():
            print >> sys.stderr, k,v
def main():
    os.chdir('../deploy')
    for hos in HOS_NAME:
        os.chdir(hos)
        status = None
        lmr3796.set_env('./doh.json')
        #dept_id = json.loads(lmr3796.dept_handler())[2].items()[0][0]
        dept_id = '60'
        #doc_id  = json.loads(lmr3796.dept_handler(dept_id))[2]['doctor'][0].items()[0][0]
        #time    = json.loads(lmr3796.doc_handler(dept_id=dept_id, doc_id=doc_id))[3]['time'][0]
        try:
            #status = json.loads(lmr3796.register(iden=IDEN, birthday=BIRTH, name=NAME,gender=GENDER, nation=ORIGIN, marriage=MARRIAGE,time=time, doc_id=doc_id, dept_id=dept_id))
            #if status['status'] != '0':
            #    raise NameError('Register')
            #status = json.loads(lmr3796.cancel(iden=IDEN, nation=ORIGIN, birthday=BIRTH, time=time, doc_id=doc_id, dept_id=dept_id, code=None))
            #if status['status'] != '0':
            #    raise NameError('Cancel')
            status = json.loads(lmr3796.num_handler(dept_id))
            for d in status['number']:
                for k,v in d.iteritems():
                    print k,v
            #print BeautifulSoup(lmr3796.get_num_page()).prettify()
            #print BeautifulSoup(lmr3796.get_num_page()).prettify()
            #if status['status'] == '1':
            #    raise NameError('Number')
        except BaseException as e:
            #print e
            #status_dump(hos, dept_id, doc_id, time, status)
            raise
        os.chdir('..')
    return 0

if __name__ == '__main__':
    exit(main())
