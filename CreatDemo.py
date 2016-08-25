# ! /usr/bin/env python
# -*- coding:utf-8 -*-

'Python module'

__author__ = 'Gao Yuhao'

try:
    input = raw_input
except:
    pass

import requests
from bs4 import BeautifulSoup
import json

page_index = input('Pls input the page_index you want to try:')
surl = 'http://www.we.com/lend/detailPage.action?loanId=' + page_index
req = requests.get(url=surl)
html = req.text.encode('utf-8')

out = open('DEMO' + page_index + '.html', 'w+')
out.write(str(html))
out.close()

def res(string):
    try:
        soup = BeautifulSoup(string, 'html.parser')
        res = soup('script', id='credit-info-data')[0].text
        return json.loads(res)
    except:
        return None

x = res(html)
if x != None and len(x) != 0:
    out = open('DEMO' + page_index + '.txt', 'w+')
    out.write(json.dumps(x, indent=4))
    out.close
else:
    pass
