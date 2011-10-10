#/usr/bin/env python
#coding=utf8

#Running PATH
RUNNING='/srv/www/hwln/'
import os, sys, web
os.chdir(RUNNING)
sys.path.append(RUNNING)
import query
urls = (
    '/', 'Mainpage',
    '/dept', 'Dept',
    '/doctor', 'Doctor',
    '/register','Register',
    '/cancelregister','Cancel',
)

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()

class Dept:
	def GET(self):
		input_data = web.input(id=None)
		return query.dept_handler(input_data.id)
class Doctor:
	def GET(self):
		input_data = web.input(id=None, deptId=None)
		return query.doc_handler(doc_id=input_data.id, dept_id=input_data.deptId)
class Register:
	def GET(self):
		'''Jizz'''
class Cancel:
	def GET(self):
		'''Jizz'''

if __name__ == "__main__":
	main()
	app.run()
	'''
	You shouldn't close the connection here because app.run()
	do something like fork() and if you conn.close()
	the running app would encounter connection reset problem.
	This is very annoying.
	'''
	
	print >> sys.stderr, ''
