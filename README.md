# Spider
基于**Python 2.7+** 编写的人人贷(WE)交易数据爬虫，默认爬取*交易序号(loanid)、用户名(user_name)、地址(address)、职业(job_type)、交易金额(amount)、利率(interest)、周期(months)、信用等级(risk_level)*和*完成度(finish_ratio)*，可以通过修改正则表达式匹配部分修改爬取内容。

爬取数据使用 SpiderWE.py 文件，修改爬取规则可以先用 CreateDemo.py 查看原网页代码。

请**不要**同时开多个线程爬取，以免对网站造成影响或IP被屏蔽。
