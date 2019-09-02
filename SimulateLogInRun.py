#这是执行程序，负责执行
from SimulateLogInLib import SimulateLogInConf
import time
import logging
# def simulate_log_in_run():
#     try:
#         i = 0
#         while True:
#             ticks_atart = time.time()
#             SimulateLogInConf.SimulateLogInConf().simulate_login_conf()
#             ticks_end = time.time()
#             print(i)
#             i = i+1
#             print(ticks_end-ticks_atart)
#             print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
#             time.sleep(30)
#     except Exception as e:
#         logging.exception(e)
#         time.sleep(30)
#         simulate_log_in_run()

if __name__ == '__main__':
    # # simulate_log_in_run()
    # i = 0
    # while True:
    #     try:
    #         ticks_atart = time.time()
    #         #微信自动确认绑定邮箱功能
    #         SimulateLogInConf.SimulateLogInConf().simulate_login_conf()
    #         ticks_end = time.time()
    #         print(i)
    #         i = i+1
    #         print(ticks_end-ticks_atart)
    #         print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    #         time.sleep(30)
    #     except Exception as e:
    #         logging.exception(e)

    #微信改密功能
    SimulateLogInConf.SimulateLogInConf().simulate_login_conf_pass()



