#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2

page_index = input(r'Pls input the page_index you want to try:')
sName = '%d' %page_index
surl = r'http://www.we.com/lend/detailPage.action?loanId='+sName
req = urllib2.Request(surl, None, {'User-Agent': 'Mozilla/5.0'})
html = urllib2.urlopen(req).read()
out = open('DEMO'+sName+'.html','w+')
out.write(html)
out.close()