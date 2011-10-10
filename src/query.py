#! /usr/bin/env python
#coding=utf8
import httplib
from httplib import HTTPConnection
from urllib import urlencode
from BeautifulSoup import BeautifulSoup
import sys
import os
import re
import json
import time
import datetime
import pickle

#Server Constants
SERVER = 'chyiwww01.chyi.doh.gov.tw'
WWW_PATH = ''
DEP_PATH = WWW_PATH + '/CHOOSEDEP1.ASP'
DOC_PATH = WWW_PATH + '/FirstReg.asp'
REG_PATH = WWW_PATH + '/PatReg.asp'
#HTTP connection basics
basic_headers = {
		'Host': SERVER,
		'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.220 Safari/535.1',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Encoding': 'gzip,deflate,sdch',
		'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
		'Accept-Charset': 'utf-8;q=0.7,*;q=0.3'
		}
basic_dataset = {}

conn = HTTPConnection(SERVER)
cookieValue = None

all_dept = None
all_doc = None

'''
all_doc[0][doc_id] returns (name, dept_id)
all_doc[1][dept_id]['name'/'id']
'''

def print_http_conn_status(conn):
	print >> sys.stderr, ''
	print >> sys.stderr, 'REQUEST INFO'
	print >> sys.stderr, method+' http://'+hostname+pathname
	print >> sys.stderr, headers
	print >> sys.stderr, dataset
	print >> sys.stderr, '------------'

	print >> sys.stderr, 'RESPONSE INFO'
	response = conn.getresponse()
	print >> sys.stderr, response.status, response.reason
	print >> sys.stderr, response.getheaders()


	print >> sys.stderr, '------------'
	print >> sys.stderr, 'RESPONSE'

def get_page( hostname, pathname='/', method='GET', headers=basic_headers, dataset=basic_dataset ):
	global cookieValue, conn
	params = urlencode(dataset)
	if method == 'GET' and params != '':
		pathname += '?'+params
	if cookieValue is not None:
		headers['Cookies'] = cookieValue

	try:
		conn.request(method, pathname, params, headers)
	except httplib.CannotSendRequest:
		conn = HTTPConnection(SERVER)
	except:
		raise
	else:
		pass

	response = conn.getresponse()
	for header in response.getheaders():
		if header[0]=='set-cookie':
			cookieValue = header[1]

	if response.status != 200:
		raise NameError( 'HTTP error code:' + str( response.status ) )

	return response.read()

def get_dept_page():
	try:
		return get_page( SERVER, DEP_PATH )
	except:
		raise

def get_doc_page(dept_id, method='GET'):
	headers = basic_headers.copy()
	dataset = basic_dataset.copy()

	try:
		dept_page = get_page( SERVER, DEP_PATH, 'GET', headers, dataset )
	except:
		raise

	headers.update({
		'Content-Type': 'application/x-www-form-urlencoded',
		'Origin': 'http://chyiwww01.chyi.doh.gov.tw',
		'Referer': 'http://chyiwww01.chyi.doh.gov.tw/CHOOSEDEP1.ASP'
		})
	dataset.update({
		'Department': dept_id,
		'hfNetregStr': ''
		})

	try:
		doc_page = get_page( SERVER, DOC_PATH, method, headers, dataset )
	except:
		raise
	return doc_page

def parse_dept_page(dept_page):
	#Encoding error on some pages....
	dept_soup = BeautifulSoup(unicode(dept_page, 'big5'))
	dept_by_code = {} 
	for dept in dept_soup.findAll('a', attrs={'alt':u'''科別'''}):
		dept_code = re.match( r"javascript:sendData\(\"(\w+)\"\)", dept['href']).group(1)
		dept_name = dept.string[:-1]
		dept_by_code[dept_code] = dept_name
	return dept_by_code

def parse_doc_page(doc_page):
	#Encoding error on some pages....
	doc_soup = BeautifulSoup(unicode(doc_page, 'big5', 'ignore'))
	space_pattern = re.compile(r'\s+')

	slots_by_doctor = {}

	for td in doc_soup.findAll('td',attrs={'class': re.compile('schedule\w'), 'headers': re.compile('b(\w+) a(\w+)')}):
		for input in td.findAll('input'):
			input_tag = str(input)
			doc_name = re.sub(space_pattern, '', input.nextSibling)
			if doc_name not in slots_by_doctor:
				slots_by_doctor[doc_name] = set()
			slots_by_doctor[doc_name].add(input_tag) 

	return slots_by_doctor

def parse_doc_input_tag(input_tag):
	#<INPUT TYPE="radio" NAME="opt" VALUE="1000928202  1  " onclick='KeypressRadio()' OnKeyPress='enterSend()'>
	value = re.search('value=\"\s*(.+?)\s*\"', input_tag)
	if value is None:
		raise NameError('Bad input_tag')
	value = value.group(1)
	YYYY = str(int(value[0:3]) + 1911)
	MM = value[3:5]
	DD = value[5:7]
	X = chr( int(value[7]) + (ord('A') - 1) )
	time = YYYY, MM, DD, X
	dep_id = value[8:10]
	doc_num_in_slot = value[-1]
	return time, id, doc_num_in_slot

def get_all_dept():
	try:
		dept_page = get_page( SERVER, DEP_PATH )
		return parse_dept_page(dept_page)
	except:
		raise

def get_all_doc(by_parse = False):
	#Department cache not available, capture it again
	global all_dept, all_doc
	try:
		if all_dept is None:
			all_dept = get_all_dept()
	except:
		raise
	#Check for cache
	by_id_file_name = 'doc_by_id.pickle'
	by_dept_file_name = 'doc_by_dept.pickle'

	#if forced by parse a page
	if by_parse:
		print >> sys.stderr, "Forced to fetch a new page."
		return get_all_doc_by_parsing(by_id_file_name, by_dept_file_name)

	#Try if cache file exist/expired or not
	try:
		id_day = datetime.datetime.fromtimestamp(os.stat(by_id_file_name).st_mtime).day
		dept_day = datetime.datetime.fromtimestamp(os.stat(by_id_file_name).st_mtime).day
		today = datetime.datetime.now().day
		if today != id_day or today != dept_day:
			return get_all_doc_by_parsing(by_id_file_name, by_dept_file_name)
	except:
		print >> sys.stderr, "Cache file expired or not found."
		return get_all_doc_by_parsing(by_id_file_name, by_dept_file_name)

	#Try if a cache file can be opened good
	try:
		by_id_file = open(by_id_file_name, 'rb')
		by_dept_file = open(by_dept_file_name, 'rb')
	except:
		print >> sys.stderr, '''Can't open cache file.'''
		return get_all_doc_by_parsing(by_id_file_name, by_dept_file_name)

	doc_by_id = pickle.load(by_id_file)
	doc_by_dept = pickle.load(by_dept_file)
	by_id_file.close()
	by_id_file.close()

	#Test if cache content is useful
	if doc_by_id is None or doc_by_dept is None:
		return get_all_doc_by_parsing(by_id_file_name, by_dept_file_name)
	return doc_by_id, doc_by_dept

def get_all_doc_by_parsing(by_id_file_name='doc_by_id.pickle', by_dept_file_name='doc_by_dept.pickle'):
	global all_dept, all_doc
	doc_by_id = {}
	doc_by_dept = {}
	print >> sys.stderr, 'Parsing doctor data from each department'
	for dept_id , dept_name in all_dept.iteritems():
		print >> sys.stderr, ('Parsing ' + dept_id + ':\t' + dept_name + '...').encode('utf8')

		#In case some department got no doctor to be reserved, do it here
		doc_by_dept[dept_id] = {}

		for doc_name, input_tag_set in parse_doc_page(get_doc_page(dept_id)).iteritems():
			doc_id = str(len(doc_by_id))
			doc_by_id[doc_id] = doc_name, dept_id, input_tag_set
			doc_by_dept[dept_id][doc_id] = doc_name

	print >> sys.stderr, 'All departments parsed!'
	by_id_file = open(by_id_file_name, 'wb')
	by_dept_file = open(by_dept_file_name, 'wb')
	pickle.dump(doc_by_id, by_id_file)
	pickle.dump(doc_by_dept, by_dept_file)
	by_id_file.close()
	by_id_file.close()
	return doc_by_id, doc_by_dept

def dept_handler(dept_id=None):
	global all_dept, all_doc
	try:
		if all_doc is None:
			all_doc = get_all_doc()
	except:
		raise
	dept_arr = None
	if dept_id is None:
		dept_arr = []
		for dept_code, dept_name in all_dept.iteritems():
			if len(all_doc[1][dept_code]) > 0:
				dept_arr.append({dept_code:dept_name})
	else:
		if all_doc is None:
			all_doc = get_all_doc()
		dept_arr = [{'id': dept_id}, {'name': all_dept[dept_id]}, {'doctor': []}]
		for doc_id, doc_name in all_doc[1][dept_id].iteritems():
			dept_arr[2]['doctor'].append({doc_id: doc_name})
		dept_arr[2]['doctor'] = sorted(dept_arr[2]['doctor'], key=lambda doc: int(doc.keys()[0]))
	return json.dumps(dept_arr, ensure_ascii=False)


def doc_handler(doc_id=None, dept_id=None):
	if (dept_id is None) != (doc_id is None):
		raise NameError('Bad dept_id or doc_id!')
	global all_dept, all_doc
	try:
		if all_doc is None:
			all_doc = get_all_doc()
	except:
		raise
	departments = set()
	doc_arr = None
	if doc_id is not None:
		if all_doc[0][doc_id][1] != dept_id:
			raise NameError('No such doctor in this department')

		doc_name, dept_id, input_tag_set = all_doc[0][doc_id]
		doc_arr = [{'id': doc_id}, {'name': doc_name},{}, {'time': []}]
		for input_tag in input_tag_set:
			time = parse_doc_input_tag(input_tag)[0]
			today = datetime.date.today()
			doc_day = datetime.date(int(time[0]), int(time[1]), int(time[2]))
			if (doc_day - today).days not in range(1, 8):
				continue
			#Not sorted, sorting is not on the spec
			doc_arr[3]['time'].append(time[0] + '-' + time[1] + '-' + time[2] + '-' + time[3])
			doc_arr[3]['time'].sort()
	else:
		doc_arr = []
		for k,v in all_doc[0].iteritems():
			doc_arr.append({k: v[0]})
		doc_arr = sorted(doc_arr, key=lambda doc: int(doc.keys()[0]))
	return json.dumps(doc_arr, ensure_ascii=False)

####Register Part####
def need_check_code():
	return False

def register(iden=None, birthday=None, name=None,
		gender=None, native=None, code=None,
		time=None, doc_id=None, dept_id=None):

	if (dept_id is None) != (doc_id is None):
		raise NameError('Bad dept_id or doc_id!')
	global all_dept, all_doc
	try:
		if all_doc is None:
			all_doc = get_all_doc()
	except:
		raise

	missing_arg = false
	missing_arr = []
	if iden is None:
		missing_arg = True
		missing_arr.add({'id':u'身分證字號'})
	if birthday is None:
		missing_arg = True
		missing_arr.add({'birthday':u'生日'})
	if time is None:
		missing_arg = True
		missing_arr.add({'time':u'看診時段'})

	if name is None:
		missing_arg = True
		missing_arr.add({'name':u'姓名'})
	if gender is None:
		missing_arg = True
		missing_arr.add({'gender':u'性別，男性填1女性填2'})
	if nation is None:
		missing_arg = True
		missing_arr.add({'native':u'本國外國，本國請填1外國請填2'})
	if need_check_code() and code is None:
		missing_arg = True
		missing_arr.add({'code':'code:http://ooxxx.ooxx'})

	if missing_arg:
		return json.dumps({'status':'2', 'message':missing_arr}, ensure_ascii=False)
	try:
		do_registration(iden, birthday, name, gender, native, code, time, doc_id, dept_id)
	except:
		return json.dumps({'status':'1', 'message':'Unknown Error'}, ensure_ascii=False)

def do_registration(iden, birthday, name, gender, native, code, time, doc_id, dept_id):
	#After getting all needed info
	dataset={
				#Required patient info
				'id_no'		:iden,
				'BirthY'	:unicode(int(re.match(r'''(\w+)-(\w+)-(\w+)''', birthday).group(1)) - 1911),
				'BirthM'	:unicode(int(re.match(r'''(\w+)-(\w+)-(\w+)''', birthday).group(2))),
				'BirthD'	:unicode(int(re.match(r'''(\w+)-(\w+)-(\w+)''', birthday).group(3))),
				'PatName'	:name,
				'sex'		:gender,
				'origid'	:nation
			}

	#There are some hidden input form needed to be fetched
	doc_page_soup = BeautifulSoup(get_doc_page(dept_id))
	hidden_input_tags = doc_page_soup.find('form', attrs={'method':'POST','name':'RegFrm'}).findAll('input', type='hidden')
	for input_tag in hidden_input_tags:
		dataset[input_tag['name']] = input_tag['value']
	
	#Simulate the javascript and fill in the missing hidden value
	dataset['opt_keycheck'] = 'Y'
	dataset['optTemp'] = '' 
	dataset['opt'] = ''
	
	#Finish the POST FORM
	button = doc_page_soup.find('input', attrs={'type':'submit','id':re.compile(r'''button(\w+)''')})	
	dataset[button['id']]=button['value']
	
	print dataset


def main():
	#Preresquities
	global all_dept, all_doc
	all_dept = get_all_dept()
	all_doc = get_all_doc()
	#print dept_handler('02')
	'''
	Test case:
	鄭逢乾, doc_id = 9, dept_id = '02'(內科), time = 100/10/14早上
	'''
	
	do_registration(iden='E123456789', birthday='1990-05-22', name=u'王小明', gender='1', native='1',
					code=False, time='10010141', doc_id='9', dept_id='02')
	dept_handler()

if __name__ == "__main__":
	main()
	conn.close()
	print >> sys.stderr, ''

