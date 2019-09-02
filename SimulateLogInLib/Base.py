import logging
import time
import random
from time import sleep
import pymssql
import re
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib import request
import requests
class Base(object):
    # 定义构造函数，定义各种属性和logging类的配置
    def __init__(self):
        #默认编码
        self.encoding = ''
        #浏览器登录后得到的cookie，也就是刚才复制的字符串
        self.cookie_str = ''
        #登录后才能访问的网页
        self.url = ''
        #登录页面
        self.loginUrl = ''
        #登录名
        self.userName = ''
        #登录密码
        self.passWord = ''
        #User-Agent
        self.user_agent = ''

        self.get_mail_href_rule = ''
        self.get_mail_href_rule_son = ''
        self.get_mail_href_rule_son_ensure = ''

        self.get_mail_href_rule_son_en = ''
        self.get_mail_href_rule_son_ensure_en = ''

        logging.basicConfig(level=logging.WARNING,  # 控制台打印的日志级别 DEBUG WARNING
                            filename='./log/' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log',
                            filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                            # a是追加模式，默认如果不写的话，就是追加模式
                            format=
                            '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                            # 日志格式
                            )

    # 数据库连接
    def db_conn(self):
        try:
            server = '192.168.6.111\mssqlzf'
            user = 'sa'
            password = 'sa@2016'
            database = 'zrhjdb'
            charset = 'utf8'
            port = '1433'
            # server = 'localhost'
            # user = 'BJUser1'
            # password = 'stock_BJ2010'
            # database = 'ZFJSSITE'
            # charset = 'utf8'
            # port = '24567'
            return pymssql.connect(host=server, user=user, password=password, database=database, charset=charset,
                                   port=port)
            # return pymssql.connect(server, user, password, database)
        except Exception as e:
            logging.exception(e)
    #获取邮件链接
    def get_mail_href_re(self,html_str):
        try:
            pattern = re.compile(self.get_mail_href_rule, re.S)
            items = re.findall(pattern, html_str)
            conn = self.db_conn()
            cursor = conn.cursor()
            for item in items:
                if '微信注册确认' in item:
                    pattern_son = re.compile(self.get_mail_href_rule_son, re.S)
                    item_href = re.findall(pattern_son, item)
                    if len(item_href) > 0:
                        # print('https://mail.yahoo.com'+item_href[0])
                        request_url = 'https://mail.yahoo.com'+item_href[0]

                        req = request.Request(request_url)
                        # 设置cookie
                        req.add_header('cookie', self.cookie_str)
                        # 设置请求头
                        req.add_header('User-Agent', self.user_agent)

                        resp = request.urlopen(req)
                        #
                        ensure_mail_str = resp.read().decode(self.encoding)
                        pattern_son_ensure = re.compile(self.get_mail_href_rule_son_ensure, re.S)
                        item_href_ensure = re.findall(pattern_son_ensure, ensure_mail_str)
                        # bindingTime = datetime.datetime.now()
                        # print(item_href_ensure[0][2])
                        response = requests.get(item_href_ensure[0][2])
                        # 防止乱码
                        response.encoding = response.apparent_encoding
                        if response.status_code == 200:
                            print(response.text)
                            if '验证成功' in response.text:
                                # 将数据存入数据库
                                cursor.execute("insert into WechatYahooMailBindingHistory values (%s,%s,CONVERT(varchar,GETDATE(),120))",
                                               (item_href_ensure[0][1], item_href_ensure[0][0]))
                                conn.commit()
                elif 'Verify your email address on WeChat' in item:

                    pattern_son = re.compile(self.get_mail_href_rule_son_en, re.S)
                    item_href = re.findall(pattern_son, item)

                    if len(item_href) > 0:
                        # print('https://mail.yahoo.com'+item_href[0])
                        request_url = 'https://mail.yahoo.com' + item_href[0]

                        req = request.Request(request_url)
                        # 设置cookie
                        req.add_header('cookie', self.cookie_str)
                        # 设置请求头
                        req.add_header('User-Agent', self.user_agent)

                        resp = request.urlopen(req)
                        #
                        ensure_mail_str = resp.read().decode(self.encoding)
                        pattern_son_ensure = re.compile(self.get_mail_href_rule_son_ensure_en, re.S)
                        item_href_ensure = re.findall(pattern_son_ensure, ensure_mail_str)
                        # bindingTime = datetime.datetime.now()
                        # print(item_href_ensure[0][2])
                        response = requests.get(item_href_ensure[0][2])
                        # 防止乱码
                        response.encoding = response.apparent_encoding
                        if response.status_code == 200:
                            print(response.text)
                            if 'Email verified successfully' in response.text:
                                # 将数据存入数据库
                                cursor.execute(
                                    "insert into WechatYahooMailBindingHistory values (%s,%s,CONVERT(varchar,GETDATE(),120))",
                                    (item_href_ensure[0][1], item_href_ensure[0][0]))
                                conn.commit()
            conn.close()
        except Exception as e:
            logging.exception(e)

    # 获取邮件链接(改密)
    def get_mail_href_re_pass(self, html_str):
        try:
            pattern = re.compile(self.get_mail_href_rule, re.S)
            items = re.findall(pattern, html_str)
            conn = self.db_conn()
            cursor = conn.cursor()
            for item in items:
                if '找回微信密码' in item:
                    pattern_son = re.compile(self.get_mail_href_rule_son, re.S)
                    item_href = re.findall(pattern_son, item)
                    if len(item_href) > 0:
                        # print('https://mail.yahoo.com'+item_href[0])
                        request_url = 'https://mail.yahoo.com' + item_href[0]

                        req = request.Request(request_url)
                        # 设置cookie
                        req.add_header('cookie', self.cookie_str)
                        # 设置请求头
                        req.add_header('User-Agent', self.user_agent)

                        resp = request.urlopen(req)
                        #
                        ensure_mail_str = resp.read().decode(self.encoding)
                        # print(ensure_mail_str)
                        pattern_son_ensure = re.compile(self.get_mail_href_rule_son_ensure, re.S)
                        item_href_ensure = re.findall(pattern_son_ensure, ensure_mail_str)
                        # print(item_href_ensure[0][2])
                        # print(item_href_ensure[0][0])

                        #item_href_ensure[0][0]邮箱

                        #模拟用户点击更改密码
                        # mobileEmulation = {'deviceName': 'iPhone 6'}
                        chrome_options = Options()
                        # chrome_options.add_experimental_option('mobileEmulation', mobileEmulation)
                        # chrome_options.add_argument("--headless")
                        browser = webdriver.Chrome(
                            executable_path=(r'C:\Users\0923\AppData\Local\Google\Chrome\Application\chromedriver.exe'),
                            options=chrome_options)
                        # 设置访问链接
                        browser.get(item_href_ensure[0][2])
                        #生成8位随机密码
                        seed = "1234567890abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ"
                        sa = []
                        for i in range(8):
                            sa.append(random.choice(seed))
                        salt = ''.join(sa)
                        #print(salt)
                        #
                        # browser.find_element_by_id("header-profile-button").click()
                        browser.find_element_by_name("password").send_keys(salt)
                        sleep(1)
                        browser.find_element_by_name("confirmpwd").send_keys(salt)
                        sleep(1)
                        browser.find_element_by_class_name("bt_action").click()
                        sleep(1)
                        change_pass_success_html = browser.page_source
                        if "您的微信密码已重设成功" in change_pass_success_html:
                            # 将数据存入数据库
                            cursor.execute(
                                "update WechatAccWechat set HasChangePass = %s,ChangeStr=%s where bindingQQ = %s",
                                (1, salt, item_href_ensure[0][0]))
                            conn.commit()


                # elif 'Verify your email address on WeChat' in item:
                #
                #     pattern_son = re.compile(self.get_mail_href_rule_son_en, re.S)
                #     item_href = re.findall(pattern_son, item)
                #
                #     if len(item_href) > 0:
                #         # print('https://mail.yahoo.com'+item_href[0])
                #         request_url = 'https://mail.yahoo.com' + item_href[0]
                #
                #         req = request.Request(request_url)
                #         # 设置cookie
                #         req.add_header('cookie', self.cookie_str)
                #         # 设置请求头
                #         req.add_header('User-Agent', self.user_agent)
                #
                #         resp = request.urlopen(req)
                #         #
                #         ensure_mail_str = resp.read().decode(self.encoding)
                #         pattern_son_ensure = re.compile(self.get_mail_href_rule_son_ensure_en, re.S)
                #         item_href_ensure = re.findall(pattern_son_ensure, ensure_mail_str)
                #         # bindingTime = datetime.datetime.now()
                #         # print(item_href_ensure[0][2])
                #         response = requests.get(item_href_ensure[0][2])
                #         # 防止乱码
                #         response.encoding = response.apparent_encoding
                #         if response.status_code == 200:
                #             print(response.text)
                #             if 'Email verified successfully' in response.text:
                #                 # 将数据存入数据库
                #                 cursor.execute(
                #                     "insert into WechatYahooMailBindingHistory values (%s,%s,CONVERT(varchar,GETDATE(),120))",
                #                     (item_href_ensure[0][1], item_href_ensure[0][0]))
                #                 conn.commit()
            conn.close()
        except Exception as e:
            logging.exception(e)