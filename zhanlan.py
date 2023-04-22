import requests
from bs4 import BeautifulSoup

import lib.request.headers as headers
import lib.spider.base_spider as base_spider
from lib.item.level import Level


def getInfo(level):
    total_page = 1
    level_list = list()
    page = 'http://www.caec.org.cn/newsList.html?id={0}'.format(level)
    print(page)
    headersData = headers.create_headers()
    response = requests.get(page, timeout=10, headers=headersData)
    html = response.content
    soup = BeautifulSoup(html, "lxml")
    # 获得总的页数
    try:
        total_page = int(soup.find('div', class_='page').find_all('a')[-2].text)
        print(total_page)
    except:
        pass
    for i in range(1, total_page + 1):
        page = 'http://www.caec.org.cn/newsList.html?id={0}&pageIndex={1}'.format(level, i)
        # print(page)
        headersData = headers.create_headers()
        response = requests.get(page, timeout=10, headers=headersData)
        html = response.content
        soup = BeautifulSoup(html, "lxml")
        # 获得每个页面class="zx" 里 ul li a 的href
        all_li = soup.find('div', class_='zx').find('ul').find_all('li')
        for li in all_li:
            href = li.find('a').get('href')
            link = 'http:' + href
            response = requests.get(link, timeout=10, headers=headersData)
            html = response.content
            link_soup = BeautifulSoup(html, "lxml")
            # 获取标题
            title = link_soup.find('h4', class_='post-title').find('div').text
            level_list.append(title)
            # desc_p_all = link_soup.find('div', class_='post-desc').findAll('p')
            # desc_div_all = link_soup.find('div', class_='post-desc').findAll('div')
            # desc_br_all = link_soup.find('div', class_='post-desc').findAll('br')
            desc_all = link_soup.find('div', class_='post-desc').text
            desc_data = list()
            desc_text = desc_all.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
            desc_data.append(desc_text)
            level_data = Level(title, desc_data)
            print(level_data.text())
            level_list.append(level_data)
    return level_list


if __name__ == "__main__":
    # level = 50
    # i = 9
    # page = 'http://www.caec.org.cn/newsList.html?id={0}&pageIndex={1}'.format(level, i)
    # print(page)
    # headersData = headers.create_headers()
    # response = requests.get(page, timeout=10, headers=headersData)
    # html = response.content
    # soup = BeautifulSoup(html, "lxml")
    # # 获得每个页面class="zx" 里 ul li a 的href
    # all_li = soup.find('div', class_='zx').find('ul').find_all('li')
    # for li in all_li:
    #     href = li.find('a').get('href')
    #     link = 'http:' + href
    #     response = requests.get(link, timeout=10, headers=headersData)
    #     html = response.content
    #     link_soup = BeautifulSoup(html, "lxml")
    #     # 获取标题
    #     title = link_soup.find('h4', class_='post-title').find('div').text
    #     # 判断是否有br
    #     desc_br_all = link_soup.find('div', class_='post-desc').text
    #     # 如何获取br标签的内容
    #     print(desc_br_all)

    # Q: What is the type of data?
    # A: list
    # Q: how to print the data
    # A: print(data)
    # Q: how to print the first element of the data
    # A: print(data[0])
    # Q: TypeError: 'dict' object is not callable
    # A: data is a list, not a dict

    csv_file = "/{0}.csv".format('level3')
    with open(csv_file, "w") as f:
        for level in getInfo(50):
            # Q: AttributeError: 'str' object has no attribute 'text'
            # A: level is a str, not a Level object
            # Q: TypeError: unsupported operand type(s) for +: 'Level' and 'str'
            # A: level.text() return a str, not a Level object
            # Q: TypeError: can only concatenate str (not "Level") to str
            # A: level.text() return a str, not a Level object
            try:
                data = level.text()
                f.write(data + "\n")
            except:
                pass

    print("Finish crawl level: level3, save data to : " + csv_file)
