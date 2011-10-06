#/usr/bin/env python
#coding=utf8
import query
def get_rand_num_from_doc_page(doc_page):
	doc_soup = BeautifulSoup(unicode(doc_page, 'big5', 'ignore'))
	target_tag = doc_soup.find('input', attrs={'type':'hidden', 'name': re.compile(r'RandNumb(\s+?)')})
	if target_tag is None:
		raise NameError('''Can't find RandNumb''')
	return str(target.name), str(target.value)

