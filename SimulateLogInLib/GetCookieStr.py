#这是获取cookies字符串的类
from SimulateLogInLib import Base
#引入selenium下的webdriver... ...
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#引入时间类，因为我们需要sleep几秒钟
from time import sleep
#引入日志类
import logging
class GetCookieStr(Base.Base):
    def get_cookie_str(self, yahooMailId):
        try:
            mobileEmulation = {'deviceName': 'iPhone 6'}
            chrome_options = Options()
            chrome_options.add_experimental_option('mobileEmulation', mobileEmulation)
            # chrome_options.add_argument("--headless")
            browser = webdriver.Chrome(executable_path=(r'C:\Users\0923\AppData\Local\Google\Chrome\Application\chromedriver.exe'), options=chrome_options)
            # 设置访问链接
            browser.get(self.loginUrl)
            # # 这是pc版的登录过程
            # # 点击登录按钮
            # browser.find_element_by_id("uh-signin").click()
            # # 输入用户名
            # browser.find_element_by_id("login-username").send_keys(self.userName)
            # # 点击“下一步”
            # browser.find_element_by_id("login-signin").click()
            # # 等待10秒，以防读取不到（#login-passwd）元素
            # sleep(10)
            # # 输入密码
            # browser.find_element_by_id("login-passwd").send_keys(self.passWord)
            # # 点击signin按钮
            # browser.find_element_by_id("login-signin").click()
            # # 这是mobile版的登录过程
            # 点击登录按钮
            browser.find_element_by_id("header-profile-button").click()
            # 点击sign in
            browser.find_element_by_id("profile-user-info-msg").click()
            # 输入用户名
            browser.find_element_by_id("login-username").send_keys(self.userName)
            # 点击“下一步”
            browser.find_element_by_id("login-signin").click()
            # 等待10秒，以防读取不到（#login-passwd）元素
            sleep(10)
            # 输入密码
            browser.find_element_by_id("login-passwd").send_keys(self.passWord)
            # 点击signin按钮
            browser.find_element_by_id("login-signin").click()
            # 获取cookie
            cookie_items = browser.get_cookies()
            cookie_str = ""
            # 组装cookie字符串
            for item_cookie in cookie_items:
                item_str = item_cookie["name"] + "=" + item_cookie["value"] + "; "
                cookie_str += item_str
            # 返回cookie字符串
            conn = self.db_conn()
            cursor = conn.cursor()
            # 将数据存入数据库
            cursor.execute("update WechatYahooMainMailBox set CookieStr=%s where Id=%s",
                           (cookie_str, yahooMailId))
            conn.commit()
            conn.close()
            return cookie_str
        except Exception as e:
            #如果报错，记录到日志中
            logging.exception(e)