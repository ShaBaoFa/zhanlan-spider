import threading
from lib.utility.date import *
import random

thread_pool_size = 50

RANDOM_DELAY = False

class BaseSpider(object):
    @staticmethod
    def random_delay():
        if RANDOM_DELAY:
            time.sleep(random.randint(0, 16))

    def __init__(self):
        # 准备日期信息，爬到的数据存放到日期相关文件夹下
        self.date_string = get_date_string()
        print('Today date is: %s' % self.date_string)
        self.mutex = threading.Lock()  # 创建锁
