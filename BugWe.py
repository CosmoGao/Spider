# -*- coding: utf-8 -*-
import re
import urllib2
import sqlite3
import os
#import xlrd
import sqlite3
 
# 打开数据库文件
 
rrdai_db = sqlite3.connect(r'C:\Users\GaoYH\Desktop\rrdai.db')
cursor = rrdai_db.cursor()
 
# 建表
 
cursor.execute('DROP TABLE IF EXISTS loanlog')
cursor.execute('CREATE TABLE loanlog (loanid varchar(8), user_id varchar(8), user_name varchar(50), address varchar(50), job_type varchar(100), borrow_id varchar(8), amount varchar(10), interest varchar(6), months varchar(3), risk_level varchar(3), finish_ratio varchar(6))')
 
#user_id, user_name, address, job_type, credit_id, borrow_id, amount, interest, months, risk_level, finish_ratio 
 
pattern = re.compile(r'"loanId":(?P<loanid>\d+).+"amount":(?P<amount>[^,]+),"interest":(?P<interest>[0-9.]+),"months":(?P<months>\d+).*"finishedRatio":(?P<finish_ratio>[^,]+).*"borrowerId":(?P<borrow_id>\d+).+"nickName":"(?P<user_name>[^"]+).+"borrowerLevel":"(?P<risk_level>[^"]+)","address":"(?P<address>[^"]*)","jobType":"(?P<job_type>[^"]*)"',re.S|re.M) 

#cursor.execute('DROP TABLE IF EXISTS loanlog')
#cursor.execute('CREATE TABLE loanlog (loanid varchar(8),amount varchar(10), intrest varchar(6), months varchar(3), risk_level varchar(3), age varchar(4), marriage varchar(6), graduation varchar(20), success varchar(4), halt varchar(4), income varchar(50), address varchar(50))')
#pattern = re.compile(r'"loanid":(?P<loanid>\d+),"amount":(?P<amount>[^,]+),"interest":(?P<interest>[0-9.]+),"months":(?P<months>\d+),"borrowerLevel":"(?P<risk_level>[^"]+)"',re.S|re.M)
#pattern = re.compile(r'"loanid":(?P<loanid>\d+),"amount":(?P<amount>[^,]+),"interest":(?P<interest>[0-9.]+),"months":(?P<months>\d+),"borrowerLevel":"(?P<risk_level>[^"]+)",年龄</span><em>(?P<age>\d+),婚姻</span><em>  (?P<marriage>..),学历</span><em>(?P<graduation>..),成功借款</span><em>(?P<success>\d+),逾期次数</span><em>(?P<halt>\d+),收入</span><em>(?P<income>.*)</em>,"address":"(?P<address>[^"]*)"',re.S|re.M)

     
def parse(url):
    req = urllib2.Request(url, None, {'User-Agent': 'Mozilla/5.0'})  #pretend to be a browser
    try:
        html = urllib2.urlopen(req).read()
        return [ m.groupdict() for m in pattern.finditer(html)]
    except:
        return None    
         
page_start = 114789
page_end = 114840
index = 1
try:
    for page_index in range (page_start,page_end):
        sName = '%d' %page_index
        surl = r'http://www.we.com/lend/detailPage.action?loanId='+sName
        print sName
        x = parse(surl)
        if x != None and len(x) != 0:
            index = index + 1
            cursor.execute('INSERT INTO loanlog (loanid, user_name, address, job_type, borrow_id, amount, interest, months, risk_level, finish_ratio ) VALUES (?,?,?,?,?,?,?,?,?,?)', (x[0]['loanid'], x[0]['user_name'].decode("utf8"), x[0]['address'].decode("utf8"), x[0]['job_type'].decode("utf8"), x[0]['borrow_id'], x[0]['amount'], x[0]['interest'], x[0]['months'], x[0]['risk_level'], x[0]['finish_ratio']))        
            if index == 50:
                index = 1
                rrdai_db.commit()
                print '50 records has been submitted!!!!!!!'       
    print 'jobes done!'
except:
    print 'there is an error at'+sName
# print x['address'].decode("utf8")
os.system("pause")