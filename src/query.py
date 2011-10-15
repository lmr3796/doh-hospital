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
NEED_CHECK_CODE = False
#Cache Constants
ALL_DEPT_FILE = 'all_dept.pickle'
ALL_DOC_BY_ID_FILE = 'all_doc_by_id.pickle'
ALL_DOC_BY_DEPT_FILE = 'all_doc_by_dept.pickle'

prev_page = None
#HTTP connection basics
basic_headers = {
		'Host': SERVER,
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.92 Sarari/535.2',
		'Connection': 'keep-alive',
		}
basic_dataset = {}
conn = None		#A HTTPConnection
cookieValue = None

all_dept = None
all_doc = None

'''
all_doc[0][doc_id] returns (name, dept_id, input_tag_set)
all_doc[1][dept_id]['name'/'id']
'''

def get_page( hostname=SERVER, pathname='/', method='GET', headers=basic_headers, dataset=basic_dataset, reset_referer=False ):
	global cookieValue, conn, prev_page
	print >> sys.stderr, '\nGetting Page: '+ method +' http://'+hostname + pathname
	params = urlencode(dataset)

	if cookieValue is not None:
		headers['Cookie'] = cookieValue

	if prev_page is not None:
		headers['Referer'] = prev_page
		print >>sys.stderr,'Referer: ' + prev_page

	if reset_referer:
		prev_page=None
	else:
		prev_page = 'http://' + hostname + pathname
		
	if method == 'GET' and params != '':
		pathname += '?'+params
	elif method == 'POST':
		headers['Content-Type'] = 'application/x-www-form-urlencoded'
		print len(headers)
		print headers
		print len(dataset)
		print params
		print ''
		
	try:
		if conn is None: 
			conn = HTTPConnection(SERVER)
		conn.request(method, pathname, params, headers)
	except httplib.CannotSendRequest:
		conn.connect()
		conn.request(method, pathname, params, headers)
		print >> sys.stderr, 'Connection reset.'
	
	response = conn.getresponse()
	print >> sys.stderr, 'HTTP/', (lambda ver: ver == 11 and '1.1' or '1.0')(response.version), response.status, response.reason
	#print response.getheaders()
	for header in response.getheaders():
		if header[0]=='set-cookie':
			cookieValue = re.match(r'''(.*);(.*)''', header[1]).group(1)
			print >>sys.stderr, 'set-cookie: ' + header[1] + ', Cookie: ' + cookieValue
	'''
	if response.status != 200:
		raise NameError( 'HTTP error code:' + str( response.status ) )
	'''
	return response.read()

def get_dept_page():
	return get_page( SERVER, DEP_PATH )

def get_doc_page(dept_id, method='GET'):
	headers = basic_headers.copy()
	dataset = basic_dataset.copy()
	
	#Request it in order to get cookies
	dept_page = get_page( SERVER, DEP_PATH, 'GET', headers, dataset )

	headers.update({
		'Origin': 'http://chyiwww01.chyi.doh.gov.tw',
		'Referer': 'http://chyiwww01.chyi.doh.gov.tw/CHOOSEDEP1.ASP'
		})
	dataset.update({
		'Department': dept_id,
		'hfNetregStr': ''
		})

	doc_page = get_page( SERVER, DOC_PATH, method, headers, dataset )
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
	value = re.search('value=\"\s*(.+?)\s*\"', input_tag)
	if value is None:
		raise NameError('Bad input_tag')
	value = value.group(1)
	YYYY = str(int(value[0:3]) + 1911)
	MM = value[3:5]
	DD = value[5:7]
	X = chr( int(value[7]) + (ord('A') - 1) )
	time = YYYY, MM, DD, X
	dept_id = value[8:10]
	doc_num_in_slot = value[-1]
	return time, dept_id, doc_num_in_slot

def get_all_dept(by_parse=False):
	#if forced by parse a page
	if by_parse:
		return get_all_dept_by_parsing()
	else:
		#Check if cache file available
		if cache_file_avail(ALL_DEPT_FILE):
			all_dept_file = open(ALL_DEPT_FILE, 'rb')
			departments = pickle.load(all_dept_file)
			all_dept_file.close()
			#Test if cache content is useful
			if departments is None:
				by_parse = True
		else:
			by_parse = True

	if by_parse:
		return get_all_dept_by_parsing()
	else:
		return departments 

	
def get_all_dept_by_parsing(all_dept_file_name = ALL_DEPT_FILE, write_cache=True):
	dept_page = get_page( SERVER, DEP_PATH )
	result = parse_dept_page(dept_page)
	try:
		all_dept_file = open(all_dept_file_name,'wb')
		pickle.dump(result,all_dept_file)
	except IOError:
		print >> sys.stderr, "Can't write cache file"
	return result

def get_all_doc(by_parse = False):
	#Department cache not available, capture it again
	global all_dept, all_doc
	if all_dept is None:
		print >>sys.stderr, 'all_dept is None'
		all_dept = get_all_dept()

	#if forced by parse a page
	if by_parse:
		print >> sys.stderr, "Forced to fetch a new page."
	else:
		#Check if cache file available
		if cache_file_avail(ALL_DOC_BY_ID_FILE) and cache_file_avail(ALL_DOC_BY_DEPT_FILE):
			by_id_file = open(ALL_DOC_BY_ID_FILE, 'rb')
			by_dept_file = open(ALL_DOC_BY_DEPT_FILE, 'rb')
			doc_by_id = pickle.load(by_id_file)
			doc_by_dept = pickle.load(by_dept_file)
			by_id_file.close()
			by_dept_file.close()
			#Test if cache content is useful
			if doc_by_id is None or doc_by_dept is None:
				by_parse = True
		else:
			print 'jizz2'
			by_parse = True

	if by_parse:
		return get_all_doc_by_parsing()
	else:
		return doc_by_id, doc_by_dept

def get_all_doc_by_parsing(by_id_file_name = ALL_DOC_BY_ID_FILE, by_dept_file_name = ALL_DOC_BY_DEPT_FILE, write_cache=True):
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
	if write_cache:
		by_id_file = open(by_id_file_name, 'wb')
		by_dept_file = open(by_dept_file_name, 'wb')
		pickle.dump(doc_by_id, by_id_file)
		pickle.dump(doc_by_dept, by_dept_file)
		by_id_file.close()
		by_id_file.close()
	return doc_by_id, doc_by_dept

def cache_file_avail(file_name):
	#Check if cache exists
	try:
		cache_stat = os.stat(file_name)
	except OSError:
		print >> sys.stderr, 'Cache file not found.'
		return False
	except:
		print >> sys.stderr, 'Unknown error stating cache file.'
		return False

	#Check if cache expired
	id_day = datetime.datetime.fromtimestamp(cache_stat.st_mtime).day
	dept_day = datetime.datetime.fromtimestamp(cache_stat.st_mtime).day
	today = datetime.datetime.now().day
	if today != id_day or today != dept_day:
		print >> sys.stderr, 'Cache expired.'
		return False
	
	#Try if a cache file can be opened good
	try:
		cache_file = open(ALL_DOC_BY_ID_FILE, 'rb')
		cache_file.close()
	except:
		print >> sys.stderr, '''Can't open cache file.'''
		return False

	return True

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

def register(iden=None, birthday=None, name=None,
		gender=None, nation=None, marriage=None, code=None,
		time=None, doc_id=None, dept_id=None):
	if (dept_id is None) != (doc_id is None):
		raise NameError('Bad dept_id or doc_id!')

	global all_dept, all_doc
	try:
		if all_doc is None:
			all_doc = get_all_doc()
	except:
		raise NameError('Error connecting to server.')

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
		missing_arr.add({'nation':u'本國外國，本國請填1外國請填2'})
	if NEED_CHECK_CODE and code is None:
		missing_arg = True
		missing_arr.add({'code':'code:http://ooxxx.ooxx'})
	if marriage is None:
		missing_arg = True
		missing_arr.add({'marriage':u'婚姻狀況，未婚請填1，已婚請填2，離婚請填3，喪偶請填4'})

	if missing_arg:
		return json.dumps({'status':'2', 'message':missing_arr}, ensure_ascii=False)
	try:
		return do_registration(iden, birthday, name, gender, nation, code, time, doc_id, dept_id)
	except:
		return json.dumps({'status':'1', 'message':'Unknown Error'}, ensure_ascii=False)

def do_registration(iden, birthday, name, gender, nation, marriage, code, time, doc_id, dept_id):
	headers = basic_headers.copy()
	#After getting all needed info
	
	dataset={}
	#There are some hidden input form needed to be fetched
	doc_page_soup = BeautifulSoup(get_doc_page(dept_id))
	all_input_tags = doc_page_soup.find('form', attrs={'method':'POST','name':'RegFrm'}).findAll('input',attrs={'type':'hidden'})
	for input_tag in all_input_tags:
		dataset[input_tag['name']] = input_tag['value']
	dataset.update({
				#Required patient info
				'idno'		:iden,
				'BirthY'	:unicode(int(re.match(r'''(\w+)-(\w+)-(\w+)''', birthday).group(1)) - 1911),
				'BirthM'	:unicode(int(re.match(r'''(\w+)-(\w+)-(\w+)''', birthday).group(2))),
				'BirthD'	:unicode(int(re.match(r'''(\w+)-(\w+)-(\w+)''', birthday).group(3))),
				'PatName'	:name,
				'sex'		:gender,
				'origid'	:nation,
				'marriage'	:marriage
			})
	
	#Simulate the javascript and fill in the missing hidden value
	'''
	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	!!!!Most important part on registration!!!!
	!!!!optTemp = id + ValueOfSlot + nation!!!!
	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	'''
	slot_value = None
	for tag in all_doc[0][doc_id][2]:
		time_match = re.match(r'''(\w+)-(\w+)-(\w+)-(\w+)''', time)
		if time_match is None:
			return json.dumps({'status':'1', 'message':'Wrong time format given by API'}, ensure_ascii=False)
		YYYY = time_match.group(1)
		MM	 = time_match.group(2)
		DD	 = time_match.group(3)
		X	 = time_match.group(4)
		#slot_pattern = re.compile("radio")
		#Matching slot of the doctor
		#print parse_doc_input_tag(tag)[0],
		#print (YYYY,MM,DD,X)
		if parse_doc_input_tag(tag)[0] == (YYYY,MM,DD,X):
			slot_value = re.search(r'''value\s*=\s*"(.+?)"''', tag).group(1)
			break;
			
	if slot_value is None:		#No matching slot for the doctor
		print 'jizz'
		return json.dumps({'status':'1', 'message':'此醫生無此看診時段'}, ensure_ascii=False)
		
	dataset['optTemp'] = iden + slot_value + nation
	dataset['opt'] = slot_value
	dataset['opt_keycheck'] = 'Y'
	
	#Finish the POST FORM
	button = doc_page_soup.find('input', attrs={'type':'submit','id':re.compile(r'''button(\w+)''')})	
	dataset[button['id']]=button['value']
	ans = ''
	for key, value in dataset.iteritems():
		dataset[key] = value.encode('big5')
		#ans += '&' + key + '=' + dataset[key] 
	print ans
	return get_page( pathname=REG_PATH, method='POST', headers=headers, dataset=dataset )

def main():
	#Preresquities
	get_page(pathname='/netreg.asp')
	get_page(pathname='/ChooseDep.asp')
	global all_dept, all_doc
	all_dept = get_all_dept()
	all_doc = get_all_doc()
	'''
	Test case:
	鄭逢乾, doc_id = 9, dept_id = '02'(內科), time = 100/10/17777777早上
	'''
	do_registration(iden='E123456789', birthday='1991-01-01', name=u'王曉明',
					gender='1', nation='1', marriage='1',
					code=False, time='2011-10-17-A', doc_id='8', dept_id='02')

if __name__ == "__main__":
	main()
	print >> sys.stderr, ''

