#! /usr/bin/env python
# coding=utf-8
import json,os
import lmr3796
NAME		=	u'王小明'
IDEN		=	'E123867366'
BIRTH		=	'1991-01-01'
ORIGIN		=	'1'
FIRST		=	'1'
MARRIAGE	=	'1'
GENDER		=	'1'

def main():
	os.chdir('../deploy/taic')
	lmr3796.set_env('./doh.json')
	dept_id	= json.loads(lmr3796.dept_handler())[2].items()[0][0]
	print dept_id
	doc_id	= json.loads(lmr3796.dept_handler(dept_id))[2]['doctor'][0].items()[0][0]
	print doc_id
	time	= json.loads(lmr3796.doc_handler(dept_id=dept_id, doc_id=doc_id))[3]['time'][1]
	print time

	print lmr3796.register(iden=IDEN, birthday=BIRTH, name=NAME,gender=GENDER, nation=ORIGIN, marriage=MARRIAGE,time=time, doc_id=doc_id, dept_id=dept_id)
	
	print lmr3796.cancel(iden=IDEN, nation=ORIGIN, birthday=BIRTH, time=time, doc_id=doc_id, dept_id=dept_id, code=None)
	return 0

if __name__ == '__main__':
	exit(main())
