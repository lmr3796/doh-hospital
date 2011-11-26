#! /usr/bin/env python
# coding=utf-8
import json,os,sys,copy
import lmr3796
from BeautifulSoup import BeautifulSoup
person_info = {
    'name':     u'王小明',
    'id':       'E123867366',
    'birthday': '1991-01-01',
    'nation':   '1',
    'first':    '1',
    'marriage': '1',
    'gender':   '1',
}

HOS_NAME    =[
                'mil',
                #'ccd',
                'chcg',
                'chis'
                'chyi',
                'fyh',
                'nant',
                'potz',
                'pntn',
                'lslp',
                #'syh',
                #'taic',
                #'tnh',
                #'tygh',
            ]
status = None
def status_dump(hos, dept_id, doc_id, time):
    global status
    print >> sys.stderr, '['+hos+']'
    print >> sys.stderr, dept_id 
    print >> sys.stderr, doc_id
    print >> sys.stderr, time
    if status is not None:
        for k,v in status.iteritems():
            print >> sys.stderr, k,v

def reg(dept_id, doc_id, time):
    global person_info, status
    info = copy.deepcopy(person_info)
    info.update({'time':time, 'doc_id':doc_id, 'dept_id':dept_id})
    status = json.loads(lmr3796.register(info))
    if status['status'] != '0':
        raise NameError('Register')
    else:
        print 'Registration succeed!' 

def can(dept_id, doc_id, time):
    global person_info, status
    info = copy.deepcopy(person_info)
    info.update({'time':time, 'doc_id':doc_id, 'dept_id':dept_id})
    status = json.loads(lmr3796.cancel(info))
    if status['status'] != '0':
        raise NameError('Cancel')
    else:
        print 'Cancelation succeed!' 

def num(dept_id):
    status = json.loads(lmr3796.num_handler(dept_id))
    if status['status'] == '1':
        raise NameError('Number')
    elif status['status'] == '0':
        for d in status['number']:
            for k,v in d.iteritems():
                print k,v
    else:
        print status['message']

def main():
    global status
    os.chdir('../deploy')
    for hos in HOS_NAME:
        os.chdir(hos)
        lmr3796.set_env('./doh.json')
        dept_id = json.loads(lmr3796.dept_handler())[2].items()[0][0]
        #dept_id = '0210'
        doc_id  = json.loads(lmr3796.dept_handler(dept_id))[2]['doctor'][0].items()[0][0]
        time    = json.loads(lmr3796.doc_handler(dept_id=dept_id, doc_id=doc_id))[3]['time'][0]
        try:
            reg(dept_id, doc_id, time) 
            can(dept_id, doc_id, time) 
            num(dept_id)
        except BaseException as e:
            print e
            status_dump(hos, dept_id, doc_id, time)
            raise
        os.chdir('..')
    return 0

if __name__ == '__main__':
    exit(main())
