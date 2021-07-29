"""
下载图书数据, readers365做的太烂了，每个作者的排版都不一样，这TM怎么爬，哭了
"""
import codecs
import time

import requests
from bs4 import BeautifulSoup
import os
import json

import fetch_proxy_ip

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
}

SLEEP_TIME_SEC = 3
save_path = 'books_365'
main_url = 'http://www.readers365.com/laoshewenji/em/001.htm'


# 没有找到资源异常
class NotFoundException(Exception):
    pass


# 下载作者的相关内容
def download_author(author_url):
    print("download_author start, url:%s" % (author_url))

    r = doRequest(author_url)

    if r == None:
        return

    charsets = get_charsets(r)
    r.encoding = charsets
    text = r.text

    soup = BeautifulSoup(text, 'html.parser')

    dict = {}

    results = soup.find_all('tr')
    for idx, tr in enumerate(results):
        if idx == 1:
            save_author_info(author_url, tr)

        if idx != 0:
            tds = tr.find_all('td')
            if len(tds) > 0:
                for _, td in enumerate(tds):
                    if len(td.contents) > 1:
                        con = td.contents[1]

                        print(con)
                        if str(type(con)) == "<class 'bs4.element.Tag'>" and str(con).startswith("<a"):
                            name = con.string
                            href = con['href']
                            if href.startswith("000"):
                                href = href[:href.index(".")]
                            else:
                                href = href[:href.index("/")]
                            dict[name] = href
    print(dict)

    save_author_download_info(author_url, dict)

    for key, value in dict.items():
        download_book(author_url + "/" + value)

    print("download_author end, url:%s" % (author_url))

# 保存作者信息
def save_author_info(author_url, tr):
    info = ""
    tds = tr.find_all('td')
    if len(tds) > 0:
        td = tds[0]
        for _, con in enumerate(td.contents):
            print(con)

            text = ""
            if str(type(con)) == "<class 'bs4.element.Tag'>" and str(con).startswith("<font"):
                text = repr(con.string)
            elif str(type(con)) == "<class 'bs4.element.NavigableString'>" and str(con) != "\n":
                text = repr(con).replace("\\xa0\\xa0\\xa0", "")

            if len(text) > 0:
                text = text[1:len(text) - 1]
                info += text + "\n"

    print(info)

    if len(info) <= 0:
        return

    dir = setup_author_dir(author_url)
    fileName = "author_info.txt"
    filePath = str.format("%s/%s" % (dir, fileName))

    if os.path.exists(filePath):
        os.remove(filePath)

    with codecs.open(filePath, 'a', encoding='UTF-8') as f:
        f.write(info)

    print("save_download_info, url:%s, filePath:%s" % (author_url, filePath))


# 保存作者文章下载信息
def save_author_download_info(author_url, dict):
    info = ""
    for key, value in dict.items():
        name = key
        url = author_url + "/" + value
        info += name + "," + url + "\n"

    if len(info) <= 0:
        return

    dir = setup_author_dir(author_url)
    fileName = "download_info.txt"
    filePath = str.format("%s/%s" % (dir, fileName))

    if os.path.exists(filePath):
        os.remove(filePath)

    with codecs.open(filePath, 'a', encoding='UTF-8') as f:
        f.write(info)

    print("save_download_info, url:%s, filePath:%s" % (author_url, filePath))


# 下载文章
def download_book(book_url):
    print("start download book, %s" % book_url)

    if checkIsSinglePageBook(book_url):
        try:
            fetch_save_book_data(book_url)
        except NotFoundException as e:
            print(e)
            print("download book failed, %s,%s" % (book_url, e))
            return
    else:
        index = 1
        while (True):
            try:
                fetch_save_book_data(getUrlWithIndex(book_url, index))

                index += 1
            except NotFoundException as e:
                print(e)
                break

    print("end download book, %s" % book_url)


# 获取并保存文章
def fetch_save_book_data(url):
    dir = setup_page_dir(url)
    fileName = url[url.rindex("/") + 1: url.rindex(".")]
    filePath = str.format("%s/%s.txt" % (dir, fileName))

    # 如果已经下载，则跳过
    if os.path.exists(filePath):
        print('已经下载过了，跳过: %s，%s' % (url, filePath))
        return

    time.sleep(SLEEP_TIME_SEC)

    print('开始请求页面url: %s' % (url))

    # 请求数据
    r = doRequest(url)
    if r == None:
        return

    charsets = get_charsets(r)
    r.encoding = charsets
    text = r.text

    soup = BeautifulSoup(text, 'html.parser')
    div = soup.find('td', attrs={'class': 'tt2'})

    if (not div):
        raise NotFoundException("not found resources")

    strArr = []

    for element in div.next_elements:
        if str(type(element)) == "<class 'bs4.element.NavigableString'>":
            elemStr = repr(element)
            elemStr = elemStr.replace("\\u3000\\u3000", "")
            elemStr = elemStr.replace("\\n", "")
            elemStr = elemStr.replace("\\r", "")
            elemStr = elemStr[1:len(elemStr) - 1]

            if elemStr == "后页":
                break

            # elemStr = elemStr.encode("utf-8").decode("gbk")

            print(elemStr)
            strArr.append(elemStr)

    # print(strArr)

    # 保存数据
    with codecs.open(filePath, 'a', encoding='UTF-8') as f:
        for txt in strArr:
            f.write(txt + "\n")


# 发起请求
def doRequest(url):
    # proxies = fetch_proxy_ip.getOneAvailableProxy()
    proxies = {}
    print('使用ip %s 请求数据' % proxies)

    r = None
    try:
        if len(proxies) > 0:
            r = requests.get(url, proxies=proxies, headers=headers, timeout=5)
        else:
            r = requests.get(url, headers=headers, timeout=5)
    except Exception as e:
        print(e)
    return r


# 获取响应内容的编码
def get_charsets(res):
    _charset = ""
    try:
        _charset = requests.utils.get_encoding_from_headers(res.headers)
        if _charset == 'ISO-8859-1':
            try:
                __charset = requests.utils.get_encodings_from_content(res.content)[0]
                if __charset:
                    _charset = __charset
                else:
                    _charset = res.apparent_encoding
            except Exception as e:
                _charset = res.apparent_encoding
    except Exception as e:
        _charset = res.apparent_encoding

    return _charset


# 确保页面存储的目录
def setup_page_dir(page_url):
    directory = save_path
    page_url = page_url.replace("http://", "")
    arr = page_url.split("/")
    for index in range(len(arr)):
        if index > 0 and index < len(arr) - 1:
            directory += "/" + arr[index]

    print(directory)

    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as e:
            pass

    return directory


# 确保作者存储的目录
def setup_author_dir(author_url):
    directory = save_path
    author_url = author_url.replace("http://", "")
    arr = author_url.split("/")
    for index in range(len(arr)):
        if index > 0:
            directory += "/" + arr[index]

    print(directory)

    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as e:
            pass

    return directory


def getUrlWithIndex(mainUrl, index):
    name = ""
    if index < 10:
        name = str.format("00%d" % index)
    elif index < 100:
        name = str.format("0%d" % index)
    else:
        name = str.format("%d" % index)
    url = str.format("%s/%s.htm" % (mainUrl, name))
    return url


def checkIsSinglePageBook(book_url):
    isSingle = False;
    if book_url.find("/000/") >= 0:
        isSingle = True
    return isSingle


if __name__ == "__main__":
    # download_book("http://www.readers365.com/laoshewenji/em")
    # download_author("http://www.readers365.com/laoshewenji")
    download_author("http://www.readers365.com/luxunquanji")
