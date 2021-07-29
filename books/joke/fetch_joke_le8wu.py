"""
get乐吧屋笑话
"""
import time

import requests
from bs4 import BeautifulSoup

from config import Configer

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
}

SLEEP_TIME_SEC = 3
save_path = 'le8wu'
pic_format_url = 'http://wap.le8wu.com/pic_%s.html'
txt_format_url = 'http://wap.le8wu.com/text/xiaohua_%s.html'

main_url = "http://wap.le8wu.com"
config_path = "config_le8wu.ini"

pic_page = 1

STATE_OK = 1
STATE_NO_CONTENT = 2
STATE_NET_ERR = 3
STATE_UNKNOWN_ERR = 4


# 没有找到资源异常
class NotFoundException(Exception):
    pass


def get_pic_datas():
    pic_page = getConfigItem("page_pic")
    page = int(pic_page)
    while (True):
        pic_url = str.format(pic_format_url % page)
        state = get_pic_data(pic_url)
        if state == STATE_NO_CONTENT:
            break
        elif state == STATE_OK:
            time.sleep(1)
            page = page + 1
        else:
            time.sleep(3)
            pass

def get_text_datas():
    pic_page = getConfigItem("page_txt")
    # while (True):
    page = 2
    txt_url = str.format(txt_format_url % page)
    get_text_data(txt_url)


def get_pic_data(url):
    print("请求url : %s" % url)

    result = doRequest(url)
    if result == None:
        return STATE_NET_ERR

    charsets = get_charsets(result)
    result.encoding = charsets
    text = result.text

    soup = BeautifulSoup(text, 'html.parser')
    divList = soup.find_all(name="li", attrs={'class': 'joke-view'})

    if divList == None:
        return STATE_NO_CONTENT

    for _, div in enumerate(divList):
        try:
            author_div = div.find(name="div", attrs={'class': 'u-info'})
            # 时间
            time = author_div.find(name="p", attrs={'class': 'j-u-name2'}).string
            # 用户名
            name_div = author_div.find(name="p", attrs={'class': 'j-u-name'})
            author_name = name_div.find(name="a").contents[0].string
            # 用户头像
            img = author_div.find(name="img")
            head_url = main_url + img["src"]

            # 标题
            title_div = div.find(name="span", attrs={'class': 'j-title'})
            a = title_div.find(name="a")
            title = a.string

            # 图片
            pic_div = div.find(name="div", attrs={'class': 'j-funny'})
            img = pic_div.find(name="img")
            pic_url = main_url + img["src"]

            # 点赞
            active_div = div.find(name="a", attrs={'class': 'j-good'})
            up_num = active_div.find(name="i").string

            # 点踩
            down_div = div.find(name="a", attrs={'class': 'j-bad'})
            down_num = down_div.find(name="i").string

            # 评论
            comments_div = div.find(name="a", attrs={'class': 'j-comment'})
            comments_num = comments_div.find(name="i").string

            print("%s, %s, %s, %s，%s, %s, %s, %s" % (time, author_name, head_url, title, pic_url, up_num, down_num, comments_num))
        except Exception as e:
            print(e)

    return STATE_OK

def get_text_data(url):
    print("请求url : %s" % url)

    result = doRequest(url)
    if result == None:
        return

    charsets = get_charsets(result)
    result.encoding = charsets
    text = result.text

    soup = BeautifulSoup(text, 'html.parser')
    divList = soup.find_all(name="li", attrs={'class': 'joke-view'})

    for _, div in enumerate(divList):
        try:
            author_div = div.find(name="div", attrs={'class': 'u-info'})
            # 时间
            time = author_div.find(name="p", attrs={'class': 'j-u-name2'}).string
            # 用户名
            name_div = author_div.find(name="p", attrs={'class': 'j-u-name'})
            author_name = name_div.find(name="a").contents[0].string
            # 用户头像
            img = author_div.find(name="img")
            head_url = main_url + img["src"]

            # 内容
            pic_div = div.find(name="div", attrs={'class': 'content-txt'})
            text = pic_div.contents[0].string

            # 点赞
            active_div = div.find(name="a", attrs={'class': 'j-good'})
            up_num = active_div.find(name="i").string

            # 点踩
            down_div = div.find(name="a", attrs={'class': 'j-bad'})
            down_num = down_div.find(name="i").string

            # 评论
            comments_div = div.find(name="a", attrs={'class': 'j-comment'})
            comments_num = comments_div.find(name="i").string

            print("%s, %s, %s, %s, %s, %s, %s" % (time, author_name, head_url, text, up_num, down_num, comments_num))
        except Exception as e:
            print(e)


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


def saveConfig(key, value):
    ini.set_item('le8wu', key, value)
    ini.save()


def getConfigItem(key):
    return ini.get_item('le8wu', key)


def loadConfig():
    global ini
    ini = Configer(config_path)

    initConfig()

    ini.cfg_load()
    ini.cfg_dump()

    page = ini.get_item("le8wu", "page_pic")
    print("page", page)


def initConfig():
    if ini.has_section("le8wu"):
        return

    ini.add_section('le8wu')
    ini.set_item('le8wu', 'page_txt', '1')
    ini.set_item('le8wu', 'page_pic', '1')
    ini.set_item('le8wu', 'page_video', '1')
    ini.save()


if __name__ == "__main__":
    loadConfig()

    get_pic_datas()
    #get_text_datas()

