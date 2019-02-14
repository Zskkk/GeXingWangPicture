from pyquery import PyQuery as pq
import requests
from requests import RequestException
import os

n = 1   #用来记录图片的数量

def get_one_pase(url):
    """
    页面源码
    :param url:
    :return:
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text
    except RequestException:
        return '页面请求失败'

def get_image(html):
    """
    得到组图的url
    :param html:
    :return:
    """
    doc = pq(html)
    items = doc('.list-main .pMain .txList_1 a.imgTitle').items()
    for item in items:
        title_url = 'https://www.woyaogexing.com' + item.attr('href')
        #print(title_url)
        get_image_url(title_url)

def get_image_url(title_url):
    """
    得到图片的url
    """
    try:
        response = requests.get(title_url)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            html = response.text
            doc = pq(html)
            items = doc('.contLeft .artCont p a img').items()
            for item in items:
                img_url = 'https:'+ item.attr('src')
                print(img_url)
                download_image(img_url)
    except RequestException:
        return '请求失败' + title_url

def download_image(img_url):
    """
    下载图片
    """
    global n
    if not os.path.exists('picture'):
        os.mkdir('picture')
    try:
        print('正在下载' + img_url)
        response = requests.get(img_url)
        if response.status_code == 200:
            filename = os.getcwd() + '\\picture\\' + str(n) + '.jpg'
            with open(filename, 'wb') as f:
                f.write(response.content)
            n = n + 1
    except RequestException:
        return '下载失败' + img_url

def main():
    for i in range(1,100):
        if i == 1:
            url = 'https://www.woyaogexing.com/tupian/'
        else:
            url = 'https://www.woyaogexing.com/tupian/index_' + str(i) + '.html'
        html = get_one_pase(url)
        get_image(html)


if __name__ == '__main__':
    main()
