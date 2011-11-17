#! /usr/bin/env python
# coding=utf-8
import json,os,sys
import lmr3796
NAME		=	u'王小明'
IDEN		=	'E123867366'
BIRTH		=	'1991-01-01'
ORIGIN		=	'1'
FIRST		=	'1'
MARRIAGE	=	'1'
GENDER		=	'1'

HOS_NAME	=[
				#'mil',
				#'chcg',
				#'chyi',
				#'syh',
				#'tnh',
				#'tygh',
				#'taic'
			]
def status_dump(hos, dept_id, doc_id, time, status):
	print >> sys.stderr, hos
	print >> sys.stderr, dept_id 
	print >> sys.stderr, doc_id
	print >> sys.stderr, time
	print >> sys.stderr, status

def main():
	os.chdir('../deploy')
	for hos in HOS_NAME:
		os.chdir(hos)
		lmr3796.set_env('./doh.json')
		dept_id	= json.loads(lmr3796.dept_handler())[2].items()[0][0]
		#print dept_id
		doc_id	= json.loads(lmr3796.dept_handler(dept_id))[2]['doctor'][0].items()[0][0]
		#print doc_id
		time	= json.loads(lmr3796.doc_handler(dept_id=dept_id, doc_id=doc_id))[3]['time'][0]
		#print time
		try:
			status = json.loads(lmr3796.register(iden=IDEN, birthday=BIRTH, name=NAME,gender=GENDER, nation=ORIGIN, marriage=MARRIAGE,time=time, doc_id=doc_id, dept_id=dept_id))
			if status['status'] != '0':
				raise NameError('Register')
			status = json.loads(lmr3796.cancel(iden=IDEN, nation=ORIGIN, birthday=BIRTH, time=time, doc_id=doc_id, dept_id=dept_id, code=None))
			if status['status'] != '0':
				raise NameError('Cancel')
		except:
			status_dump(hos, dept_id, doc_id, time, status)
			raise
		os.chdir('..')
	return 0

if __name__ == '__main__':
	exit(main())
