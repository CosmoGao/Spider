# -*- coding: utf-8 -*-
import re
import urllib2
import sqlite3
import os
#import xlrd
import sqlite3
 
# 打开数据库文件
 
WE_db = sqlite3.connect(r'.\WE.db')
cursor = WE_db.cursor()
 
# 建表
 
cursor.execute('DROP TABLE IF EXISTS loanlog')
cursor.execute('CREATE TABLE loanlog (loanid,user_name varchar(50), address varchar(50), job_type varchar(100), amount varchar(10), interest varchar(6), months varchar(3), risk_level varchar(3), finish_ratio varchar(6))')
 
#正则匹配

pattern = re.compile(r'"loanId":(?P<loanid>\d+).+"amount":(?P<amount>[^,]+),"interest":(?P<interest>[0-9.]+),"months":(?P<months>\d+).*"finishedRatio":(?P<finish_ratio>[^,]+).*"nickName":"(?P<user_name>[^"]+).+"borrowerLevel":"(?P<risk_level>[^"]+)","address":"(?P<address>[^"]*)","jobType":"(?P<job_type>[^"]*)"',re.S|re.M) 

#定义爬虫函数
     
def parse(url):
    req = urllib2.Request(url, None, {'User-Agent': 'Mozilla/5.0'})  #pretend to be a browser
    try:
        html = urllib2.urlopen(req).read()
        return [ m.groupdict() for m in pattern.finditer(html)]
    except:
        return None    
         
#自定义爬虫起始点

page_start = input('Please input the number you want to start:')
page_end = input('Then input the number you want to stop:')+1

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
            cursor.execute('INSERT INTO loanlog (loanid, user_name, address, job_type, amount, interest, months, risk_level, finish_ratio ) VALUES (?,?,?,?,?,?,?,?,?)', (x[0]['loanid'], x[0]['user_name'].decode("utf8"), x[0]['address'].decode("utf8"), x[0]['job_type'].decode("utf8"), x[0]['amount'], x[0]['interest'], x[0]['months'], x[0]['risk_level'], x[0]['finish_ratio']))        
            if index == 50:
                index = 0
                WE_db.commit()
                print '50 records has been submitted.'       
    WE_db.commit()
    print 'jobs done!'
    
except:
    print 'there is an error at'+sName


os.system("pause")