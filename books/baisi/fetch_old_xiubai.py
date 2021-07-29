#!/usr/bin/python
# coding:utf-8

"""
get嗅事百科
"""
import json
import sys
import time
from os import path

import requests
import random

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from config import Configer

from baisi.sql import insert_joke_xiubai
from baisi.sql import check_has_joke_xiubai

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
}

img_url = "https://m2.qiushibaike.com/article/list/imgrank?page=1&count=30"
video_url = "https://m2.qiushibaike.com/article/list/video?page=1&count=30"
text_url = "https://m2.qiushibaike.com/article/list/text?page=1&count=30"
day_url = "https://m2.qiushibaike.com/article/list/day?page=1&count=30"

config_path = "config_old_xiubai.ini"

STATE_OK = 1
STATE_NO_CONTENT = 2
STATE_NET_ERR = 3
STATE_UNKNOWN_ERR = 4

CHECK_RECORD = True
MAX_RETRY_COUNT = 15
SLEEP_TIME = 8 * 60 * 60

theme_id_list = []

# 没有找到资源异常
class NotFoundException(Exception):
    pass

# 全量更新数据
def get_full_datas():
    types = ["text", "imgrank", "video"]
    for type in types:
        page = 1
        retry_count = 0
        while True:
            wait_time = random.randint(5, 6)
            time.sleep(wait_time)

            state = inner_get_theme_content(type, page)

            if state == STATE_NO_CONTENT:
                print("当前theme没有内容了,type：%s" % type)
                break
            elif state == STATE_OK:
                page += 1
                retry_count = 0
                pass
            elif state == STATE_NET_ERR:
                print("网络错误，重试，重试次数%d， type：%s" % (retry_count, type))
                retry_count += 1
                if retry_count > 10:
                    print("已达最大重试次数，中断当前获取,type：%s" % type)
                    break
                time.sleep(10)
                pass

# 增量更新数据,会不停执行
def get_incremental_datas():
    types = ["text", "imgrank", "video"]

    while True:
        pre_time = time.time()
        print("开始一次增量更新，当前时间：%s" % timestamp2Str(time.time()))

        init_update_count_map()

        for type in types:
            print("获取type：%s的数据：" % type)
            try:
                page = 1
                retry_count = 0
                while True:
                    wait_time = random.randint(5, 6)
                    time.sleep(wait_time)

                    state, is_all_repeat = inner_get_theme_content(type, page)

                    if state == STATE_OK:
                        page += 1

                        if is_all_repeat:
                            # 如果获取的所有信息都是重复的，则进行重试下一页
                            retry_count += 1
                            print("获取数据重复，重试，重试次数：%d，type：%s" % (retry_count, type))
                        else:
                            retry_count = 0

                        pass
                    elif state == STATE_NO_CONTENT:
                        retry_count += 1
                        print("获取内容为空，重试，重试次数：%d，type：%s" % (retry_count, type))

                        time.sleep(10)

                        pass
                    elif state == STATE_NET_ERR:
                        print("网络错误，重试，重试次数：%d， type：%s" % (retry_count, type))
                        retry_count += 1

                        time.sleep(10)
                        pass

                    # 超过最大重试次数，中断当前类型请求
                    if retry_count > MAX_RETRY_COUNT:
                        print("超过最大重试次数：%d，中断当前获取,type：%s" % (retry_count, type))
                        break

            except Exception as e:
                print("当前更新出错：", e)

        cost_time = time.time() - pre_time
        sleep_time = SLEEP_TIME
        print("完成一次增量更新，耗时:%d秒，当前时间:%s，休眠%d秒" % (cost_time, timestamp2Str(time.time()), sleep_time))

        print_update_count_map()

        # 增量更新一次之后，休息一段时间，下次再更新
        time.sleep(sleep_time)

def inner_get_theme_content(type, page):
    theme_url = str.format("https://m2.qiushibaike.com/article/list/%s?page=%d&count=30" % (type, page))
    print("theme_url : %s" % theme_url)

    result = doRequest(theme_url)
    if result == None:
        return STATE_NET_ERR, False
    text = result.text
    data = None
    try:
        data = json.loads(text)
    except NotFoundException as e:
        print(e)
        return STATE_UNKNOWN_ERR, False

    # print(data)

    if data == None:
        return STATE_NET_ERR, False

    if not "count" in data:
        print(text)
        return STATE_NO_CONTENT, False

    count = data['count']
    list = data['items']
    size = len(list)
    if size == 0:
        print(text)
        return STATE_NO_CONTENT, False

    joke_list = []

    print("type:%s，page:%d, count:%d" % (type, page, count))
    for i in range(size):
        item = list[i]
        #print(item)

        id = item['id']
        text = item['content']
        user = item['user']
        cate = ""
        comment = item['comments_count']
        up = item['votes']['up']
        down = abs(item['votes']['down'])
        forward = item['share_count']
        passtime = timestamp2Str(item['published_at'])

        obj_url = ""
        download_url = ""
        thumb_url = ""
        width = 0
        height = 0
        duration = 0
        topcomments = ""

        if type == "text":
            pass
        elif type == "imgrank":
            if item['format'] == "multi":
                # 跳过，不处理多图情况
                continue
            else:
                type = item['format']

            if 'high_url' in item:
                download_url = obj_url = item['high_url']
            if 'low_url' in item:
                thumb_url = item['low_url']
            if 'image_size' in item:
                width = item['image_size']['m'][0]
                height = item['image_size']['m'][1]

            pass
        elif type == "video":
            if 'high_url' in item:
                download_url = obj_url = item['high_url']
            if 'pic_url' in item:
                thumb_url = item['pic_url']
            if 'image_size' in item:
                width = item['image_size']['m'][0]
                height = item['image_size']['m'][1]
                duration = item['image_size']['m'][2]

            pass

        if 'hot_comment' in item:
            top_comments = item['hot_comment']
            comments = []
            content = top_comments["content"]
            uid = top_comments['user']["uid"]
            name = top_comments['user']["login"]
            head = top_comments['user']["medium"]
            comments.append({"content":content, "uid":uid, "name":name, "head":head})
            topcomments = json.dumps(comments, ensure_ascii=False)

        joke_info = {}
        joke_info["id_from_src"] = id
        joke_info["theme_id"] = ""
        joke_info["type"] = type
        joke_info["text"] = text
        if user != None:
            joke_info["user_id"] = user["uid"]
            joke_info["user_name"] = user['login']
            joke_info["user_head"] = user['medium']
        else:
            joke_info["user_id"] = ""
            joke_info["user_name"] = ""
            joke_info["user_head"] = ""
        joke_info["src"] = "xiubai"
        joke_info["up"] = up
        joke_info["down"] = down
        joke_info["comment"] = comment
        joke_info["forward"] = forward
        joke_info["passtime"] = passtime
        joke_info["cate"] = cate
        # TODO 这里需要填充url
        joke_info["obj_url"] = obj_url
        joke_info["download_url"] = download_url
        joke_info["thumb_url"] = thumb_url
        joke_info["width"] = width
        joke_info["height"] = height
        joke_info["duration"] = duration
        joke_info["top_comments"] = topcomments
        joke_list.append(joke_info)

    success_count = 0
    is_all_repeat = True
    for joke in joke_list:
        has_joke = False
        if CHECK_RECORD:
            has_joke = check_has_joke_xiubai(joke['id_from_src'])
        if not has_joke:
            # 插入信息到数据库
            insert_joke_xiubai(joke)

            print("插入新记录, id_from_src:%s" % joke['id_from_src'])
            is_all_repeat = False

            save_update_count_map(type, 1)
            success_count += 1

        else:
            print("已经存在记录, id_from_src:%s" % joke['id_from_src'])

    saveThemeConfig(type, success_count)

    return STATE_OK, is_all_repeat


# 发起请求
def doRequest(url):
    # proxies = fetch_proxy_ip.getOneAvailableProxy()
    proxies = {}
    if len(proxies) > 0 :
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

def saveThemeConfig(type, num):
    if not ini.has_section(type):
        ini.add_section(type)

    if not ini.has_item(type, "fetch_times"):
        ini.set_item(type, "fetch_times", "0")
    fetch_times = int(ini.get_item(type, "fetch_times"))
    fetch_times += 1

    if not ini.has_item(type, "fetch_num"):
        ini.set_item(type, "fetch_num", "0")
    fetch_num = int(ini.get_item(type, "fetch_num"))
    fetch_num += num

    ini.set_item(type, "fetch_times", str(fetch_times))
    ini.set_item(type, "fetch_num", str(fetch_num))
    ini.save()


def getConfigItem(key):
    return ini.get_item('xiubai', key)


def loadConfig():
    global ini
    ini = Configer(config_path)

    ini.cfg_load()
    ini.cfg_dump()

def timestamp2Str(timestamp):
    time_local = time.localtime(timestamp)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt

def init_update_count_map():
    global type_update_count_map
    type_update_count_map = {}

def save_update_count_map(type, update_count):
    if update_count <= 0:
        return
    if not type in type_update_count_map:
        type_update_count_map[type] = 0
    pre_count = type_update_count_map[type]
    type_update_count_map[type] = pre_count + update_count

def print_update_count_map():
    total_count = 0
    for (type, count) in type_update_count_map.items():
        print("更新type：%s，更新数量：%d" % (type, count))
        total_count += count
    print("更新总数量：%d" % (total_count))

if __name__ == "__main__":
    loadConfig()

    # get_full_datas()
    get_incremental_datas()
