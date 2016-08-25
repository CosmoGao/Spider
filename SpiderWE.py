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
import sqlite3

# 打开数据库文件
WE_db = sqlite3.connect(r'./WE.db')
cursor = WE_db.cursor()

# 建表
cursor.execute('DROP TABLE IF EXISTS loanlog')
cursor.execute(
    'CREATE TABLE loanlog (loanid INT PRIMARY KEY,user_name VARCHAR(50), address VARCHAR(50), job_type VARCHAR(100), amount VARCHAR(10), interest VARCHAR(6), months VARCHAR(3), risk_level VARCHAR(3), finish_ratio VARCHAR(6))')


# 定义爬虫函数
def parse(url):
    req = requests.get(url=url)
    html = req.text.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    try:
        res = soup('script', id='credit-info-data')[0].text
        return json.loads(res)
    except:
        return None


# 自定义爬虫起始点
page_start = int(input('Please input the number you want to start:'))
page_end = int(input('Then input the number you want to stop:')) + 1

# 导入数据库
index = 0

try:
    for page_index in range(page_start, page_end):
        surl = r'http://www.we.com/lend/detailPage.action?loanId=' + str(page_index)
        print(page_index)
        x = parse(surl)
        if x != None and len(x) != 0:
            index = index + 1
            cursor.execute(
                'INSERT INTO loanlog (loanid, user_name, address, job_type, amount, interest, months, risk_level, finish_ratio ) VALUES (?,?,?,?,?,?,?,?,?)',
                (x['data']['loan']['loanId'], x['data']['loan']['nickName'], x['data']['loan']['address'],
                 x['data']['loan']['jobType'], x['data']['loan']['amount'], x['data']['loan']['interest'],
                 x['data']['loan']['months'], x['data']['loan']['borrowerLevel'], x['data']['loan']['finishedRatio']))
            if index == 50:
                index = 0
                WE_db.commit()
                print('50 records has been submitted.')
    WE_db.commit()
    print('jobs done!')

except:
    print('there is an error at' + str(page_index))

try:
    input('Press ENTER to exit.')
except:
    pass
