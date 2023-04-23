import sys
from lib.utility.version import PYTHON_3

levels = {
    '48': '一级水平',
    '49': '二级水平',
    '50': '三级水平',
}


def create_prompt_text():
    """
    根据已有城市中英文对照表拼接选择提示信息
    :return: 拼接好的字串
    """
    level_info = list()
    count = 0
    for id, ch_name in levels.items():
        count += 1
        level_info.append(id)
        level_info.append(": ")
        level_info.append(ch_name)
        if count % 4 == 0:
            level_info.append("\n")
        else:
            level_info.append(", ")
    return 'Which level do you want to crawl?\n' + ''.join(level_info)


def get_chinese_level(id):
    """
    拼音拼音名转中文城市名
    :param id: id
    :return: 中文
    """
    return levels.get(id, None)


def get_level() -> object:
    level = None
    # 允许用户通过命令直接指定
    # Q: sys.argv 是什么?
    # A: sys.argv 是一个列表，包含了命令行参数
    if len(sys.argv) < 2:
        print("Wait for your choice.")
        # 让用户选择爬取哪个level
        prompt = create_prompt_text()
        # 判断Python版本
        if not PYTHON_3:  # 如果小于Python3
            level = raw_input(prompt)
        else:
            level = input(prompt)
    elif len(sys.argv) == 2:
        level = str(sys.argv[1])
        print("Level is: {0}".format(level))
    else:
        print("At most accept one parameter.")
        exit(1)

    chinese_level = get_chinese_level(level)
    if chinese_level is not None:
        message = 'OK, start to crawl ' + get_chinese_level(level)
        print(message)
    else:
        print("No such level, please check your input.")
        exit(1)
    return level


if __name__ == '__main__':
    print(get_chinese_level("48"))
