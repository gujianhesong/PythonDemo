#!/usr/bin/python
# coding:utf-8

"""
get嗅事百科
"""
import json
import random
import sys
import time
from os import path

import requests

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from config import Configer

from baisi.sql import insert_joke_xiubai, open_db, close_db
from baisi.sql import check_has_joke_xiubai

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
}

config_path = "config_xiubai.ini"

STATE_OK = 1
STATE_NO_CONTENT = 2
STATE_NET_ERR = 3
STATE_UNKNOWN_ERR = 4

CHECK_RECORD = False
MAX_RETRY_COUNT = 30
SLEEP_TIME = 1 * 60 * 60

main_ids = [121400000,121300000,121200000,121100000,121000000]


# 没有找到资源异常
class NotFoundException(Exception):
    pass


# 增量更新数据,会不停执行
def get_range_datas():
    pre_time = time.time()

    init_update_count_map()

    for main_id in main_ids:
        print("开始获取main_id：%d范围的数据，当前时间：%s" % (main_id, timestamp2Str(time.time())))

        retry_count = 0
        page = 0
        last_id = getLastId(main_id)
        if last_id >= main_id:
            page = last_id - main_id + 1

        global last_cost_time, last_upd_time
        last_cost_time = getCostTime(main_id)
        last_upd_time = time.time()

        while True:
            wait_time = random.randint(1, 2)
            time.sleep(wait_time)

            if page >= 100000:
                print("main_id：%d范围的数据获取完成！！！" % main_id)
                break

            state = inner_get_theme_content(main_id, page)

            if state == STATE_OK:
                page += 1
                retry_count = 0

                pass
            elif state == STATE_NO_CONTENT:
                page += 1
                retry_count += 1
                print("获取内容为空，重试，重试次数：%d，main_id：%d" % (retry_count, main_id))

                pass
            elif state == STATE_NET_ERR:
                print("网络错误，重试，重试次数：%d， main_id：%d" % (retry_count, main_id))
                retry_count += 1

                time.sleep(10)
                pass
            elif state == STATE_UNKNOWN_ERR:
                print("未知错误，重试，重试次数：%d， main_id：%d" % (retry_count, main_id))
                retry_count += 1

                time.sleep(3)
                pass

            # 超过最大重试次数，中断当前类型请求
            if retry_count > MAX_RETRY_COUNT:
                print("超过最大重试次数：%d，中断当前获取, main_id：%d" % (retry_count, main_id))
                break

        print_update_count_map()

        cost_time = time.time() - pre_time
        sleep_time = SLEEP_TIME
        print("完成一次更新，耗时:%d秒，当前时间:%s，休眠%d秒" % (cost_time, timestamp2Str(time.time()), sleep_time))

        # 增量更新一次之后，休息一段时间，下次再更新
        time.sleep(sleep_time)


def inner_get_theme_content(main_id, page):
    try:
        id = main_id + page
        main_id = str(main_id)

        theme_url = str.format("https://m2.qiushibaike.com/article/%d" % (id))
        print("theme_url : %s" % theme_url)

        result = doRequest(theme_url)
        if result == None:
            return STATE_NET_ERR
        text = result.text
        data = None
        try:
            data = json.loads(text)
        except NotFoundException as e:
            print(e)
            return STATE_UNKNOWN_ERR

        # print(data)

        if data == None:
            return STATE_NET_ERR

        if not "article" in data:
            print(text)
            return STATE_NO_CONTENT

        item = data['article']

        # print(item)

        id = item['id']
        content = item['content']
        user = item['user']
        cate = ""
        comment = item['comments_count']
        up = item['votes']['up']
        down = abs(item['votes']['down'])
        forward = item['share_count']
        passtime = timestamp2Str(item['published_at'])
        format = item['format']

        obj_url = ""
        download_url = ""
        thumb_url = ""
        width = 0
        height = 0
        duration = 0
        topcomments = ""

        if format == "word":
            format = "text"
            pass
        elif format == "image" or format == "gif":
            if 'high_url' in item:
                download_url = obj_url = item['high_url']
            if 'low_url' in item:
                thumb_url = item['low_url']
            if 'image_size' in item:
                width = item['image_size']['m'][0]
                height = item['image_size']['m'][1]
            pass
        elif format == "video":
            if 'high_url' in item:
                download_url = obj_url = item['high_url']
            if 'pic_url' in item:
                thumb_url = item['pic_url']
            if 'image_size' in item:
                width = item['image_size']['m'][0]
                height = item['image_size']['m'][1]
                duration = item['image_size']['m'][2]
            pass
        elif format == "multi":
            print("不处理format is multi, id_from_src:%s" % id)
            pass

        if 'hot_comment' in item:
            top_comments = item['hot_comment']
            comments = []
            comments_content = top_comments["content"]
            uid = top_comments['user']["uid"]
            name = top_comments['user']["login"]
            head = top_comments['user']["medium"]
            comments.append({"content": comments_content, "uid": uid, "name": name, "head": head})
            topcomments = json.dumps(comments, ensure_ascii=False)

        joke_info = {}
        joke_info["id_from_src"] = id
        joke_info["theme_id"] = ""
        joke_info["type"] = format
        joke_info["text"] = content
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

        success_count = 0
        has_joke = False

        try:
            open_db()

            if CHECK_RECORD:
                has_joke = check_has_joke_xiubai(joke_info['id_from_src'])
            if not has_joke:
                # 插入信息到数据库
                insert_joke_xiubai(joke_info)

                print("插入新记录, id_from_src:%s" % joke_info['id_from_src'])

                save_update_count_map(main_id, 1)
                success_count += 1
            else:
                print("已经存在记录, id_from_src:%s" % joke_info['id_from_src'])
        finally:
            close_db()

        saveThemeConfig(main_id, success_count, id)
        if success_count > 0:
            return STATE_OK
        else:
            return STATE_NO_CONTENT
    except Exception as e:
        print("当前更新出错：", e)

    return STATE_UNKNOWN_ERR


# 发起请求
def doRequest(url):
    # proxies = fetch_proxy_ip.getOneAvailableProxy()
    proxies = {}
    if len(proxies) > 0:
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


def saveThemeConfig(type, num, id):
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

    fetch_ratio = "百分之%.2f" % (float(fetch_num) / (id % 100000 + 1) * 100)
    cost_time = int(last_cost_time + time.time() - last_upd_time)

    ini.set_item(type, "fetch_times", str(fetch_times))
    ini.set_item(type, "fetch_num", str(fetch_num))
    ini.set_item(type, "last_id", str(id))
    ini.set_item(type, "update_time", timestamp2Str(time.time()))
    ini.set_item(type, "fetch_ratio", fetch_ratio)
    ini.set_item(type, "cost_time", str(cost_time))
    ini.save()


def getLastId(type):
    type = str(type)
    try:
        if not ini.has_section(type):
            return 0
        if not ini.has_item(type, "last_id"):
            return 0
        last_id = int(ini.get_item(type, "last_id"))
        return last_id
    except Exception as e:
        print(e)
    return 0


def getCostTime(type):
    type = str(type)
    try:
        if not ini.has_section(type):
            return 0
        if not ini.has_item(type, "cost_time"):
            return 0
        cost_time = int(ini.get_item(type, "cost_time"))
        return cost_time
    except Exception as e:
        print(e)
    return 0


def getConfigItem(key):
    key = str(key)
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


def save_update_count_map(main_id, update_count):
    if update_count <= 0:
        return
    if not main_id in type_update_count_map:
        type_update_count_map[main_id] = 0
    pre_count = type_update_count_map[main_id]
    type_update_count_map[main_id] = pre_count + update_count


def print_update_count_map():
    total_count = 0
    for (type, count) in type_update_count_map.items():
        print("更新type：%s，更新数量：%d" % (type, count))
        total_count += count
    print("更新总数量：%d" % (total_count))


if __name__ == "__main__":
    loadConfig()

    get_range_datas()
