from SimulateLogInLib import Base
import sys
import io
from urllib import request
import logging
class SimulateLogIn(Base.Base):
    def simulate_login(self):
        try:
            # print(1)
            # 改变标准输出的默认编码
            # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=self.encoding)
            # print(2)
            req = request.Request(self.url)
            # 设置cookie
            req.add_header('cookie', self.cookie_str)
            # 设置请求头
            req.add_header('User-Agent', self.user_agent)

            resp = request.urlopen(req)
            #打印出我们获得的网页源码，这里大家可以按照自己的逻辑去处理，不一定是打印出来
            return resp.read().decode(self.encoding)
        except Exception as e:
            logging.exception(e)
