#这是模拟登陆配置页
#首先导入我们想要继承的类
from SimulateLogInLib import SimulateLogIn
from SimulateLogInLib import GetCookieStr
from SimulateLogInLib import Base
import logging
#这里我们采用多继承的方式继承上面两个类
class SimulateLogInConf(SimulateLogIn.SimulateLogIn, GetCookieStr.GetCookieStr, Base.Base):
    def simulate_login_conf(self):
        try:
            # 默认编码
            conn = self.db_conn()
            cursor = conn.cursor()
            # self.get_mail_href_rule = 'data-test-id="read">.*?href="(.*?)".*?微信注册确认'
            self.get_mail_href_rule = '<tr data-test-id="message-list-item"(.*?)</tr>'
            self.get_mail_href_rule_son = 'data-test-id="unread">.*?href="(.*?)".*?微信注册确认'
            self.get_mail_href_rule_son_en = 'data-test-id="unread">.*?href="(.*?)".*?Verify your email address on WeChat'
            self.get_mail_href_rule_son_ensure = '微信正在尝试绑定邮件地址(.*?)到你的帐号(.*?)。</p>.*?href="(.*?)"'
            self.get_mail_href_rule_son_ensure_en = 'WeChat is trying to link the email \((.*?)\) with your WeChat account \((.*?)\).*?</p>.*?href="(.*?)"'
            self.encoding = 'utf8'
            # self.encoding = 'GBK'
            # self.encoding = 'gb18030'
            #登录页
            self.loginUrl = 'https://www.yahoo.com'
            cursor.execute('select * from WechatYahooMainMailBox where IsDel=0 and IsBindingMail=1')
            values = cursor.fetchall()
            for item in values:
                # print(item[1])
                # print(item[6])
                #yahoo主邮箱id
                self.yahooMainMailId = item[0]
                # 登录名
                self.userName = item[1]
                #登录密码
                self.passWord = item[6] #'Zfjs1234'
                # print(item[7])
                if item[7] == '0':
                    # print('调用方法获取cookie')
                    # 浏览器登录后得到的cookie，也就是刚才复制的字符串
                    cookies_str = self.get_cookie_str(item[0])
                    self.cookie_str = cookies_str
                else:
                    # print('从数据库获取cookie')
                    self.cookie_str = item[7]
                # print(self.cookie_str)
                # 想要访问的目标网页
                #https://mail.yahoo.com/mb/folders/1?.src=ym&reason=unexpected_ymv&folderType=INBOX&offset=20
                #将链接改为上面的地址，第一页offset=0，第二页offset=10，第三页offset=20... ...
                #在SimilateLogIn中做一个for循环，循环的替换offset的值，一般三页就差不多了
                #要选取内容的话，我们就统一使用正则做匹配
                self.url = 'https://mail.yahoo.com'
                # User-Agent
                self.user_agent = 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'
                #运行login方法
                # print(self.simulate_login())
                SignIn = 'Sign in to Yahoo'
                if SignIn in self.simulate_login():
                    # print('和猜想一样！')
                    # print(self.simulate_login())
                    # print('重新登录获取cookie')
                    cookies_str_si = self.get_cookie_str(item[0])
                    self.cookie_str = cookies_str_si
                for ItemPage in ['0', '10', '20']:
                    self.url = 'https://mail.yahoo.com/mb/folders/1?.src=ym&reason=unexpected_ymv&folderType=INBOX&offset='+ItemPage
                    # print(self.url)
                    htmlstr = self.simulate_login()
                    self.get_mail_href_re(htmlstr)
                    # print(self.get_mail_href(htmlstr))
        except Exception as e:
            logging.exception(e)
    def simulate_login_conf_pass(self):
        try:
            # 默认编码
            conn = self.db_conn()
            cursor = conn.cursor()

            self.get_mail_href_rule = '<tr data-test-id="message-list-item"(.*?)</tr>'
            self.get_mail_href_rule_son = 'data-test-id="unread">.*?href="(.*?)".*?找回微信密码'
            self.get_mail_href_rule_son_en = 'data-test-id="unread">.*?href="(.*?)".*?Verify your email address on WeChat'
            self.get_mail_href_rule_son_ensure = '>To</span>.*?>(.*?)</span>.*?Hi,.*?>(.*?)</span>.*?我们协助您找回密码.*?href="(.*?)"'
            self.get_mail_href_rule_son_ensure_en = 'WeChat is trying to link the email \((.*?)\) with your WeChat account \((.*?)\).*?</p>.*?href="(.*?)"'
            self.encoding = 'utf8'
            #登录页
            self.loginUrl = 'https://www.yahoo.com'
            cursor.execute('select * from WechatYahooMainMailBox where IsDel=0')
            values = cursor.fetchall()
            for item in values:
                #yahoo主邮箱id
                self.yahooMainMailId = item[0]
                # 登录名
                self.userName = item[1]
                #登录密码
                self.passWord = item[6] #'Zfjs1234'
                # print(item[7])
                if item[7] == '0':
                    # print('调用方法获取cookie')
                    # 浏览器登录后得到的cookie，也就是刚才复制的字符串
                    cookies_str = self.get_cookie_str(item[0])
                    self.cookie_str = cookies_str
                else:
                    # print('从数据库获取cookie')
                    self.cookie_str = item[7]
                # print(self.cookie_str)
                # 想要访问的目标网页
                #https://mail.yahoo.com/mb/folders/1?.src=ym&reason=unexpected_ymv&folderType=INBOX&offset=20
                #将链接改为上面的地址，第一页offset=0，第二页offset=10，第三页offset=20... ...
                #在SimilateLogIn中做一个for循环，循环的替换offset的值，一般三页就差不多了
                #要选取内容的话，我们就统一使用正则做匹配
                self.url = 'https://mail.yahoo.com'
                # User-Agent
                self.user_agent = 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'
                #运行login方法
                # print(self.simulate_login())
                SignIn = 'Sign in to Yahoo'
                if SignIn in self.simulate_login():
                    # print('和猜想一样！')
                    # print(self.simulate_login())
                    # print('重新登录获取cookie')
                    cookies_str_si = self.get_cookie_str(item[0])
                    self.cookie_str = cookies_str_si
                for ItemPage in ['0', ]:
                    self.url = 'https://mail.yahoo.com/mb/folders/1?.src=ym&reason=unexpected_ymv&folderType=INBOX&offset='+ItemPage
                    # print(self.url)
                    htmlstr = self.simulate_login()
                    self.get_mail_href_re_pass(htmlstr)
                    # print(self.get_mail_href(htmlstr))
        except Exception as e:
            logging.exception(e)
