import sys
from lib.utility.version import PYTHON_3

provinces = {
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


def create_prompt_text():
    """
    根据已有城市中英文对照表拼接选择提示信息
    :return: 拼接好的字串
    """
    province_info = list()
    count = 0
    for id, ch_name in provinces.items():
        count += 1
        province_info.append(id)
        province_info.append(": ")
        province_info.append(ch_name)
        if count % 4 == 0:
            province_info.append("\n")
        else:
            province_info.append(", ")
    return 'Which province do you want to crawl?\n' + ''.join(province_info)


def get_chinese_province(id):
    """
    拼音拼音名转中文城市名
    :param id: id
    :return: 中文
    """
    return provinces.get(id, None)


def get_province() -> object:
    province = None
    # 允许用户通过命令直接指定
    # Q: sys.argv 是什么?
    # A: sys.argv 是一个列表，包含了命令行参数
    if len(sys.argv) < 2:
        print("Wait for your choice.")
        # 让用户选择爬取哪个province
        prompt = create_prompt_text()
        # 判断Python版本
        if not PYTHON_3:  # 如果小于Python3
            province = raw_input(prompt)
        else:
            province = input(prompt)
    elif len(sys.argv) == 2:
        province = str(sys.argv[1])
        print("Province is: {0}".format(province))
    else:
        print("At most accept one parameter.")
        exit(1)

    chinese_province = get_chinese_province(province)
    if chinese_province is not None:
        message = 'OK, start to crawl ' + get_chinese_province(province)
        print(message)
    else:
        print("No such province, please check your input.")
        exit(1)
    return province


if __name__ == '__main__':
    print(get_chinese_province("48"))
