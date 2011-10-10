#! /usr/bin/env python

import os
import query

os.system("rm *.pickle -f")
query.get_all_doc('true')
os.system("chown www-data:www-data *.pickle")
exit(0)
