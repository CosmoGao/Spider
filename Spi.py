# -*- coding: utf-8 -*-  
#---------------------------------------  
#   程序：爬虫  
#   版本：0.1  
#   作者：
#   日期：2013-05-14  
#   语言：Python 2.7  
#   操作：输入带分页的地址，去掉最后面的数字，设置一下起始页数和终点页数。  
#   功能：下载对应页码内的所有页面并存储为html文件。  
#---------------------------------------  


import sqlite3
import win32crypt
import os

def get_chrome_cookies(url):
    os.system('copy "C:\\Users\\GaoYH\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies" D:\\python-chrome-cookies')
    conn = sqlite3.connect("d:\\python-chrome-cookies")
    ret_list = []
    ret_dict = {}
    for row in conn.execute("select host_key, name, path, value, encrypted_value from cookies"):
        if row[0] != url:
            continue
        ret = win32crypt.CryptUnprotectData(row[4], None, None, None, 0)
        ret_list.append((row[1], ret[1]))
        ret_dict[row[1]] = ret[1].decode()
    conn.close()
    os.system('del "D:\\python-chrome-cookies"')
    return ret_dict


   
import string, urllib2  
   
#定义百度函数  
def spider(url,begin_page,end_page):     
    for i in range(begin_page, end_page+1):  
        sName = string.zfill(i,5) + '.html'#自动填充成六位的文件名  
        print '正在下载第' + str(i) + '个网页，并将其存储为' + sName + '......'  
        f = open(sName,'w+')  
        m = urllib2.urlopen(url + str(i),cookies=get_chrome_cookies('.we.com')).read()  
        f.write(m)  
        f.close()  
   
   
#-------- 在这里输入参数 ------------------  
  
# 这个是山东大学的百度贴吧中某一个帖子的地址  
#bdurl = 'http://tieba.baidu.com/p/2296017831?pn='  
#iPostBegin = 1  
#iPostEnd = 10  
  
#bdurl = str(raw_input(u'请输入贴吧的地址，去掉pn=后面的数字：\n'))  
#begin_page = int(raw_input(u'请输入开始的页数：\n'))  
#end_page = int(raw_input(u'请输入终点的页数：\n'))  
#-------- 在这里输入参数 ------------------  
url = 'http://www.we.com/lend/detailPage.action?loanId='
begin_page = 1
end_page = 5 
#调用  
spider(url,begin_page,end_page)  