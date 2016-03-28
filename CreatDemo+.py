#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib    
import urllib2  
import cookielib
import os

#初始化一个CookieJar来处理Cookie的信息#  
cookie = cookielib.CookieJar()  
  
#创建一个新的opener来使用我们的CookieJar#  
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))  

#自定义账号密码
l_username = raw_input('Please input your username:')
l_password = raw_input('Then input the password:')
os.system('cls')
                       
#需要POST的数据#  
postdata=urllib.urlencode({    
    'j_username':'%s' %l_username,    
    'j_password':'%s' %l_password    
})  
  
req = urllib2.Request(    
    url = 'https://www.we.com/j_spring_security_check',    
    data = postdata  
)  
  
#登录账号
result = opener.open(req)  

#定义测试页面
page_index = input(r'Pls input the page_index you want to try:')
sName = '%d' %page_index
surl = r'http://www.we.com/lend/detailPage.action?loanId='+sName
html=opener.open(surl).read()

#输出网页
out = open('DEMO'+sName+'.html','w+')
out.write(html)
out.close()
