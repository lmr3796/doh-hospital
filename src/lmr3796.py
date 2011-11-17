#! /usr/bin/env python
#coding=utf8
import httplib
from httplib import HTTPConnection
from urllib import urlencode
from BeautifulSoup import BeautifulSoup
import sys, os, re, web, copy, traceback
import json, time, datetime, pickle

#LOCAL_SERVER_PATH = '/srv/www/doh'
LOCAL_SERVER_PATH = os.path.dirname(__file__)

#Server Constants
SERVER   ='' 
WWW_PATH ='' 
DEP_PATH ='' 
DOC_PATH ='' 
REG_PATH ='' 
CAN_PATH ='' 
NEED_CHECK_CODE = False
#Cache Constants
ALL_DEPT_FILE = 'all_dept.pickle'
ALL_DOC_BY_ID_FILE = 'all_doc_by_id.pickle'
ALL_DOC_BY_DEPT_FILE = 'all_doc_by_dept.pickle'

prev_page = None
#HTTP connection basics
basic_headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.92 Sarari/535.2',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Encoding': 'gzip,deflate',
		'Accept-Language': 'zh-TW,en-us;q=0.7,en;q=0.3',
		'Accept-Charset': 'UTF-8,*'
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

def set_env(path_file):
	global SERVER, WWW_PATH, DEP_PATH, DOC_PATH, REG_PATH, CAN_PATH, NEED_CHECK_CODE
	global conn, prev_page, cookieValue, all_dept, all_doc
	f = open(path_file, 'r')
	path = json.loads(f.read())
	if path['NEED_CHECK_CODE'] == 'True':
		need = True
	else:
		need = False 
	SERVER   = path['SERVER']
	WWW_PATH = path['WWW_PATH']
	DEP_PATH = WWW_PATH + path['DEP_PATH']
	DOC_PATH = WWW_PATH + path['DOC_PATH']
	REG_PATH = WWW_PATH + path['REG_PATH']
	CAN_PATH = WWW_PATH + path['CAN_PATH']
	NEED_CHECK_CODE = need
	cookieValue = None
	prev_page = None
	all_dept = None
	all_doc = None
	if conn is not None and isinstance(conn, HTTPConnection):
		conn.close()
	conn = HTTPConnection(SERVER)
	f.close()
	#index page of it
	u'''
	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	!!!!!!一定要先戳NETREG1.asp!!!!!
	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	'''
	get_page(SERVER,pathname=WWW_PATH + '/NETREG1.asp',dataset={'mode':''})

def plot_http_response_info(response=None, sent_headers=None):
	if response is None:
		return
	print >> sys.stderr, '======================REQUEST INFO======================'
	print >> sys.stderr, 'HTTP/1.1' if response.version == 11 else 'HTTP/1.0', response.status, response.reason
	if sent_headers is not None:
		print >> sys.stderr, '                =====REQUEST HEADER=====                '
	for k,v in sent_headers.iteritems():
		print >> sys.stderr, k+':', v
	print >> sys.stderr, ''
	if response.getheaders() is not None:
		print >> sys.stderr, '                =====RESPONSE HEADER====                '
		for k,v in response.getheaders():
			print >> sys.stderr, k+':', v
		print >> sys.stderr, ''

def get_page( hostname=SERVER, pathname='/', method='GET', headers=copy.deepcopy(basic_headers),
				dataset=copy.deepcopy(basic_dataset), reset_referer=False ):
	global cookieValue, conn, prev_page
	if hostname is None:
		raise NameError('SERVER not defined')
	params = urlencode(dataset)
	if method == 'GET' and params != '':
		pathname += '?'+params

	print >> sys.stderr, method, hostname+pathname
	
	if method == 'POST':
		headers['Content-Type'] = 'application/x-www-form-urlencoded'
		print >> sys.stderr, params

	if cookieValue is not None:
		headers['Cookie'] = cookieValue
	
	if prev_page is not None and not reset_referer:
		headers['Referer'] = prev_page
	
	headers['Host'] = SERVER	
	prev_page = 'http://' + hostname + pathname
	try:
		if conn is None: 
			conn = HTTPConnection(SERVER)
		conn.request(method, pathname, params, headers)
		#print >> sys.stderr, headers
	except httplib.CannotSendRequest:
		conn.connect()
		conn.request(method, pathname, params, headers)
		print >> sys.stderr, 'Connection reset.'
	
	response = conn.getresponse()
	
	#Check if required to set cookies
	for header in response.getheaders():
		if header[0]=='set-cookie':
			cookieValue = re.match(r'''(.*);(.*)''', header[1]).group(1)
	
	if response.status != 200:
		plot_http_response_info(response, headers)
		raise NameError( 'HTTP error code:' + str( response.status ) )

	return response.read()

def get_dept_page():
	get_page(pathname=WWW_PATH+'/ChooseDep.asp', reset_referer=True)
	return get_page(SERVER, DEP_PATH)

def get_doc_page(dept_id, method='POST'):
	dataset={'Department': dept_id,	'hfNetregStr': ''}
	doc_page = get_page( hostname=SERVER, pathname=DOC_PATH, method=method, dataset=dataset)
	return doc_page


def parse_dept_page(dept_page):
	#Encoding error on some pages....
	dept_soup = BeautifulSoup(unicode(dept_page, 'big5'))
	dept_by_code = {} 
	for dept in dept_soup.findAll('a', attrs={'alt':u'''科別'''}):
		dept_code = re.match( r"javascript:sendData\(\"(\w+)\"\)", dept['href']).group(1)
		dept_name = dept.string.strip()
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
	dept_page = get_dept_page()
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
		all_dept = get_all_dept(True)

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
		
		#Try to make doctor id stable rather than decided by parsing order
		doc_list = parse_doc_page(get_doc_page(dept_id)).items()
		
		#In case some department got no doctor to be reserved
		if len(doc_list) == 0:
			continue
		doc_list = sorted(doc_list, key=lambda tup: tup[1])
		doc_by_dept[dept_id] = {}
		for doc_name, input_tag_set in doc_list:
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
	global all_dept, all_doc, DEP_PATH
	try:
		if all_doc is None:
			all_doc = get_all_doc()
	except:
		raise

	dept_arr = None
	if dept_id is None:
		dept_arr = []
		for dept_code, dept_name in all_dept.iteritems():
			if all_doc[1].has_key(dept_code):
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

	missing_arg = False
	missing_arr = []
	if iden is None:
		missing_arg = True
		missing_arr.append({'id':u'身分證字號'})
	if birthday is None:
		missing_arg = True
		missing_arr.append({'birthday':u'生日'})
	if time is None:
		missing_arg = True
		missing_arr.append({'time':u'看診時段'})

	if name is None:
		missing_arg = True
		missing_arr.append({'name':u'姓名'})
	if gender is None:
		missing_arg = True
		missing_arr.append({'gender':u'性別，男性填1女性填2'})
	if nation is None:
		missing_arg = True
		missing_arr.append({'nation':u'本國外國，本國請填1外國請填2'})
	if NEED_CHECK_CODE and code is None:
		missing_arg = True
		missing_arr.append({'code':'code:http://ooxxx.ooxx'})
	if marriage is None:
		missing_arg = True
		missing_arr.append({'marriage':u'婚姻狀況，未婚請填1，已婚請填2，離婚請填3，喪偶請填4'})

	if missing_arg:
		return json.dumps({'status':'2', 'message':missing_arr}, ensure_ascii=False)
	try:
		return do_registration(iden, birthday, name, gender, nation, marriage, code, time, doc_id, dept_id)
	except Exception:
		traceback.print_exc(Exception, file=sys.stderr)
		return json.dumps({'status':'1', 'message':'Unknown Error'}, ensure_ascii=False)

def do_registration(iden, birthday, name, gender, nation, marriage, code, time, doc_id, dept_id):
	headers = basic_headers.copy()
	#After getting all needed info
	dataset={}
	#There are some hidden input form needed to be fetched
	doc_page = get_doc_page(dept_id)
	doc_page_soup = BeautifulSoup(doc_page)		#Use POST, the server seems to POST first to reg.
	#print >> sys.stderr, doc_page_soup.prettify()
	all_input_tags = doc_page_soup.find('form', attrs={'method':'POST','name':'RegFrm'}).findAll('input')
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
		if parse_doc_input_tag(tag)[0] == (YYYY,MM,DD,X):
			slot_value = re.search(r'''value\s*=\s*"(.+?)"''', tag).group(1)
			break;
			
	if slot_value is None:		#No matching slot for the doctor
		return json.dumps({'status':'1', 'message':'此醫生無此看診時段'}, ensure_ascii=False)
		
	dataset['optTemp'] = iden + slot_value + nation
	dataset['opt'] = slot_value
	dataset['opt_keycheck'] = 'Y'
	
	#Finish the POST FORM
	button = doc_page_soup.find('input', attrs={'type':'submit','id':re.compile(r'''button(\w+)''')})	
	dataset[button['id']]=button['value']
	for key, value in dataset.iteritems():
		dataset[key] = value.encode('big5')

	succ_page_soup = BeautifulSoup(get_page( SERVER,pathname=REG_PATH, method='POST', headers=headers, dataset=dataset ))
	try:
		number = succ_page_soup.find(text=re.compile(u'''就診序號''')).nextSibling.string.strip()
		return json.dumps({'status':'0', 'message':number})
	except:
		msg = succ_page_soup.find('font', attrs={'class':'noteMsg'})
		if msg is not None:
			msg = unicode(msg.find(text=True));
			print >> sys.stderr, msg
			return json.dumps({'status':'1', 'message':msg})
		else:
			return json.dumps({'status':'1', 'message':'Unknown error.'})

def cancel(iden=None, nation=None, birthday=None, time=None, doc_id=None, dept_id=None, code=None):
	if (dept_id is None) != (doc_id is None):
		raise NameError('Bad dept_id or doc_id!')

	global all_dept, all_doc
	try:
		if all_doc is None:
			all_doc = get_all_doc()
	except:
		raise NameError('Error connecting to server.')

	missing_arg = False
	missing_arr = []
	if iden is None:
		missing_arg = True
		missing_arr.append({'id':u'身分證字號'})
	if birthday is None:
		missing_arg = True
		missing_arr.append({'birthday':u'生日'})
	if time is None:
		missing_arg = True
		missing_arr.append({'time':u'看診時段'})
	if nation is None:
		missing_arg = True
		missing_arr.append({'nation':u'本國外國，本國請填1外國請填2'})
	if NEED_CHECK_CODE and code is None:
		missing_arg = True
		missing_arr.append({'code':'code:http://ooxxx.ooxx'})

	if missing_arg:
		return json.dumps({'status':'2', 'message':missing_arr}, ensure_ascii=False)
	return do_cancel_registration(iden, nation, birthday, time, dept_id)

def do_cancel_registration(iden, nation, birthday, time, dept_id, code=None):
	can_page_soup = BeautifulSoup(get_page(SERVER,pathname=CAN_PATH))
	
	dataset={}
	try:
		all_input_tags = can_page_soup.find('form', attrs={'method':'POST','name':'RegFrm'}).findAll('input')
	except:
		print can_page_soup
		raise
	for input_tag in all_input_tags:
		if input_tag.has_key('name'):
			if input_tag.has_key('value'):
				dataset[input_tag['name']] = input_tag['value']
			else:
				dataset[input_tag['name']] = ''

	dataset.update({
				#Required patient info
				'idno'		:iden,
				'origid'	:nation,
				'BirthY'	:unicode(int(re.match(r'''(\w+)-(\w+)-(\w+)''', birthday).group(1)) - 1911),
				'BirthM'	:unicode(int(re.match(r'''(\w+)-(\w+)-(\w+)''', birthday).group(2))),
				'BirthD'	:unicode(int(re.match(r'''(\w+)-(\w+)-(\w+)''', birthday).group(3))),
				})
	
	#Finish the POST FORM
	for key, value in dataset.iteritems():
		dataset[key] = value.encode('big5')
	
	can_page_soup = BeautifulSoup(get_page(SERVER,method='POST', dataset=dataset, pathname=REG_PATH))
	'''
		Processing Second Page
	'''
	dataset = {}
	#get_page(pathname='/NETREG1.asp',dataset={'mode':''})
	time_match = re.match(r'(\w+)-(\w+)-(\w+)-(\w+)',time)
	YYY = str(int(time_match.group(1)) - 1911)
	MM = time_match.group(2)
	DD = time_match.group(3)
	X = str(ord(time_match.group(4)) - ord('A') + 1)
	opt_value_pattern = YYY + MM + DD + X + dept_id + r'.*'
	slot_found = False
	for form in can_page_soup.findAll('form', attrs={'method':'POST', 'name':'RegFrm'}):
		record = form.nextSibling
		tag = record.find('input', attrs={'name':'opt', 'value':re.compile(opt_value_pattern)}) 
		if tag is None:
			continue
		else:
			slot_found = True
			for input_tag in record.findAll('input'):
				if input_tag.has_key('name'):
					if input_tag.has_key('value'):
						dataset[input_tag['name']] = input_tag['value']
					else:
						dataset[input_tag['name']] = '' 
			break
	if not slot_found:
		return json.dumps({'status':'1', 'message':u'無此掛號資訊'}, ensure_ascii=False)

	#Finish the POST FORM
	for key, value in dataset.iteritems():
		dataset[key] = value.encode('big5')
	can_reg_soup = BeautifulSoup((get_page(pathname=REG_PATH, method='POST', dataset=dataset)))
	if can_reg_soup.find(text=re.compile(u'取消掛號成功')) is not None:
		return json.dumps({'status':'0'})
	else:
		return json.dumps({'status':'1', 'message':'Unknown error'})

#############################################################################
####################!!!!!!!!!!!!!!!!!#WSGI!!!!!!!!!!!!!!!!!!#################
#############################################################################
urls = (
    '/(\w+)/dept', 'Dept',
    '/(\w+)/doctor', 'Doctor',
    '/(\w+)/register','Register',
    '/(\w+)/cancel_register','Cancel',
	'/(\w+)/', 'BaseRequest',
	'/(.+)', 'BaseRequest',

)

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()

class BaseRequest:
	def __init__(self):
		web.header('Content-Type', 'text/html; charset=utf-8')
		self.request_path = re.search(r'(/\w+)/.*',web.ctx.path)
		if self.request_path is not None:
			self.request_path = self.request_path.group(1)
			running = LOCAL_SERVER_PATH + self.request_path 
			os.chdir(running)
			#print >> sys.stderr, 'Requesting:', request_path, 'and running at', os.getcwd()
			set_env(running + '/doh.json')
	
	def GET(self, name):
		return u'行政院衛生署網路掛號格式API' +('' if self.request_path is None else (': '+ self.request_path[1:]))

class Dept(BaseRequest):
	def GET(self, name):
		input_data = web.input(id=None)
		try:
			return dept_handler(input_data.id)
		except KeyError:
			all_dept = get_all_dept(True)
			all_doc = get_all_doc(True)
			return dept_handler(input_data.id)
			

class Doctor(BaseRequest):
	def GET(self, name):
		input_data = web.input(id=None, deptId=None)
		try:
			return doc_handler(doc_id=input_data.id, dept_id=input_data.deptId)
		except KeyError:
			all_dept = get_all_dept(True)
			all_doc = get_all_doc(True)
			return doc_handler(doc_id=input_data.id, dept_id=input_data.deptId)

class Register(BaseRequest):
	def GET(self, name):
		input_data = web.input(doctor=None, dept=None, time=None, id=None, birthday=None, first=None, name=None,
								gender=None, nation=None, marriage=None )
		try:
			return register(iden=input_data.id, birthday=input_data.birthday, name=input_data.name,
							gender=input_data.gender, nation=input_data.nation, marriage=input_data.marriage,
							time=input_data.time, doc_id=input_data.doctor, dept_id=input_data.dept)
		except KeyError:
			all_dept = get_all_dept(True)
			all_doc = get_all_doc(True)
			return register(iden=input_data.id, birthday=input_data.birthday, name=input_data.name,
							gender=input_data.gender, nation=input_data.nation, marriage=input_data.marriage,
							time=input_data.time, doc_id=input_data.doctor, dept_id=input_data.dept)
class Cancel(BaseRequest):
	def GET(self, name):
		input_data = web.input(doctor=None, dept=None, time=None, id=None, birthday=None, nation=None)
		try:
			return cancel(iden=input_data.id, birthday=input_data.birthday, nation=input_data.nation, 
							doc_id=input_data.doctor, dept_id=input_data.dept, time=input_data.time)
		except KeyError:
			all_dept = get_all_dept(True)
			all_doc = get_all_doc(True)
			return cancel(iden=input_data.id, birthday=input_data.birthday, nation=input_data.nation, 
							doc_id=input_data.doctor, dept_id=input_data.dept, time=input_data.time)

if __name__ == "__main__":
	app.run()
	'''
	You shouldn't close the connection here because app.run()
	do something like fork() and if you conn.close()
	the running app would encounter connection reset problem.
	This is very annoying.
	'''
	
	print >> sys.stderr, ''
