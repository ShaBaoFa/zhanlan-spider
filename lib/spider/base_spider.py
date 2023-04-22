import threading
from lib.utility.date import *
import random

thread_pool_size = 50

RANDOM_DELAY = False
province_data = {
    '59': '北京',
    '60': '上海',
    '61': '天津',
    '63': '重庆',
    '64': '河北',
    '65': '山西',
    '66': '内蒙古',
    '67': '辽宁',
    '68': '吉林',
    '69': '黑龙江',
    '70': '江苏',
    '71': '浙江',
    '72': '安徽',
    '73': '福建',
    '74': '江西',
    '75': '山东',
    '76': '河南',
    '78': '湖北',
    '80': '湖南',
    '81': '广东',
    '82': '广西',
    '83': '海南',
    '84': '四川',
    '85': '贵州',
    '86': '云南',
    '87': '西藏',
    '88': '陕西',
    '89': '甘肃',
    '90': '青海',
    '91': '宁夏',
    '92': '新疆',
    '93': '台湾',
    '94': '香港',
    '96': '钓鱼岛',
    '98': '海外',
}

class BaseSpider(object):
    @staticmethod
    def random_delay():
        if RANDOM_DELAY:
            time.sleep(random.randint(0, 16))

    def __init__(self):
        # 准备日期信息，爬到的数据存放到日期相关文件夹下
        self.province = province_data
        self.date_string = get_date_string()
        print('Today date is: %s' % self.date_string)

        self.mutex = threading.Lock()  # 创建锁

    def create_prompt_text(self):
        """
        根据已有城市中英文对照表拼接选择提示信息
        :return: 拼接好的字串
        """
        province_info = list()
        count = 0
        for province_id, province_name in self.province.items():
            count += 1
            province_info.append(province_id)
            province_info.append(": ")
            province_info.append(province_name)
            if count % 4 == 0:
                province_info.append("\n")
            else:
                province_info.append(", ")
        return 'Which province do you want to crawl?\n' + ''.join(province_info)
