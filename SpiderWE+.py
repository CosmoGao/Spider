#! /usr/bin/env python
# -*- coding: utf-8 -*-

'爬虫实例(需登录)'

__author__ = 'Gao Yuhao'

import re
import urllib
import urllib2
import sqlite3
import cookielib

# 打开数据库文件
WE_db = sqlite3.connect(r'./WE+.db')
cursor = WE_db.cursor()
 
# 建表
cursor.execute('DROP TABLE IF EXISTS loanlog')
cursor.execute('CREATE TABLE loanlog (loanid int primary key, userid int, user_name varchar(50), age int, address varchar(20), graduation varchar(20),marriage varchar(20), job_type varchar(50), income varchar(100), success int, overdue int, risk_level varchar(8), borrowtype varchar(50), amount varchar(10), months int, interest varchar(8),  finish_ratio varchar(8))')
 
#定义正则表达式匹配规则
pattern = re.compile(r'"user":(?P<userid>\d+).*"loanId":(?P<loanid>\d+).+"borrowType":"(?P<borrowtype>[^"]+).+"amount":(?P<amount>[^,]+),"interest":(?P<interest>[0-9.]+),"months":(?P<months>\d+).+"finishedRatio":(?P<finish_ratio>[^,]+).+"nickName":"(?P<user_name>[^"]+).+"borrowerLevel":"(?P<risk_level>[^"]+)","address":"(?P<address>[^"]*)","jobType":"(?P<job_type>[^"]*)".+\xe5\xb9\xb4\xe9\xbe\x84</span><em>(?P<age>\d+)</em>.*\xe5\xad\xa6\xe5\x8e\x86</span><em>(?P<graduation>.+)</em>.*\xe5\xa9\x9a\xe5\xa7\xbb</span><em>  (?P<marriage>.+\xe5\xa9\x9a).*\xe6\x88\x90\xe5\x8a\x9f\xe5\x80\x9f\xe6\xac\xbe</span><em>(?P<success>\d+).*\xe9\x80\xbe\xe6\x9c\x9f\xe6\xac\xa1\xe6\x95\xb0</span><em>(?P<overdue>\d+).*\xe6\x94\xb6\xe5\x85\xa5</span><em>(?P<income>.+\xe5\x85\x83)</em></div></td>\n',re.S|re.M) 

#定义爬虫函数
def parse(url):
    req = opener.open(url) 
    try:
        html = req.read()
        return [ m.groupdict() for m in pattern.finditer(html)]
    except:
        return None    

#自定义内容
l_username = raw_input('Please input your username:')
l_password = raw_input('Then input the password:')
os.system('cls')
page_start = input('Please input the number you want to start:')
page_end = input('Then input the number you want to stop:')+1

#初始化cookiejar
cookie = cookielib.CookieJar()  
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))  
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

#导入数据库
index = 0
try:
    for page_index in range (page_start,page_end):
        sName = '%d' %page_index
        surl = r'http://www.we.com/lend/detailPage.action?loanId='+sName
        print sName
        x = parse(surl)
        if x != None and len(x) != 0:
            index = index + 1
            cursor.execute('INSERT INTO loanlog (loanid, userid, user_name, age, address, graduation, marriage, job_type, income, success, overdue, risk_level, borrowtype, amount, months, interest, finish_ratio) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ', (x[0]['loanid'], x[0]['userid'], x[0]['user_name'].decode('utf-8'), x[0]['age'], x[0]['address'].decode('utf-8'), x[0]['graduation'].decode('utf-8'), x[0]['marriage'].decode('utf-8'), x[0]['job_type'].decode('utf-8'), x[0]['income'].decode('utf-8'), x[0]['success'], x[0]['overdue'], x[0]['risk_level'], x[0]['borrowtype'].decode('utf-8'), x[0]['amount'], x[0]['months'], x[0]['interest'], x[0]['finish_ratio']))        
            if index == 50:
                index = 0
                WE_db.commit()
                print '50 records has been submitted.'       
    WE_db.commit()
    print 'jobs done!'
    
except:
    print 'there is an error at'+sName

try:
    input(u'按回车键退出')
except:
    pass