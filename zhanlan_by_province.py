import os

import requests
from bs4 import BeautifulSoup

import lib.request.headers as headers
import lib.item.province as province
import lib.zone.province as Province


def getInfo(province_id):
    total_page = 1
    province_list = list()
    page = 'http://www.caec.org.cn/newsList.html?id={0}'.format(province_id)
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
        page = 'http://www.caec.org.cn/newsList.html?id={0}&pageIndex={1}'.format(province_id, i)
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
            province_list.append(title)
            # desc_p_all = link_soup.find('div', class_='post-desc').findAll('p')
            # desc_div_all = link_soup.find('div', class_='post-desc').findAll('div')
            # desc_br_all = link_soup.find('div', class_='post-desc').findAll('br')
            # for p in desc_p_all:
            #     print('=====================')
            #     wenben = p.text.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
            #     # wenben 为 空的时候，不打印
            #     if wenben:
            #         print(wenben)
            desc_all = link_soup.find('div', class_='post-desc').text
            desc_text = desc_all\
                .replace('\r', '')\
                .replace('\n', '')\
                .replace('\t', '')\
                .replace(' ', '')\
                .replace('\xa0', '')\
                .replace('\u200b', '')\
                .replace('\xad', '')
            province_data = province.Province(title, desc_text)
            # print(province_data.text())
            province_list.append(province_data)
    return province_list


if __name__ == "__main__":
    # province = 50
    # i = 9
    # page = 'http://www.caec.org.cn/newsList.html?id={0}&pageIndex={1}'.format(province, i)
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
    province_data = Province.get_province()
    province_chinese = Province.get_chinese_province(province_data)
    # 将csv_file的路径设置为当前文件夹
    csv_file = os.path.join(os.path.dirname(__file__), province_chinese + ".csv")
    with open(csv_file, "w") as f:
        provinces = getInfo(province_data)
        # 获取provinces有多少个元素
        print("一共{0}条数据".format(len(provinces)))
        for province in provinces:
            try:
                data = province.text()
                f.write(data + "\n")
            except:
                print("==================================")
                # 判断province是不是一个list
                # 如果是str 打印
                if isinstance(province, str):
                    print(province)
                else:
                    data = province.text()
                    print(data)
                    f.write(data + "\n")
                print("==================================")
                pass

    print("Finish crawl province: {0} save data to : ".format(province_chinese) + csv_file)
