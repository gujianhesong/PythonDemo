#!/usr/bin/python
# coding:utf-8

"""
get百思不得姐
"""
import json
import random
import sys
import time
from os import path

import requests

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from config import Configer

from baisi.sql import check_has_joke, open_db, close_db
from baisi.sql import insert_joke

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
}

classify_url = "http://d.api.budejie.com/forum/subscribe/budejie-android-6.9.3.json?market=360zhushou&ver=6.9.3&visiting=&os=5.1.1&appname=baisibudejie&client=android&udid=866405077133126&mac=26%3A24%3A0f%3A92%3A2c%3A33"

config_path = "config_baisi.ini"

CHECK_RECORD = True
MAX_RETRY_COUNT = 3
SLEEP_TIME = 8 * 60 * 60

pic_page = 1

STATE_OK = 1
STATE_NO_CONTENT = 2
STATE_NET_ERR = 3
STATE_UNKNOWN_ERR = 4

TYPE_NEW = 1
TYPE_JINGXUAN = 2
TYPE_HOT = 3

theme_id_list = []


# 没有找到资源异常
class NotFoundException(Exception):
    pass


def get_classify():
    result = doRequest(classify_url)
    if result == None:
        return STATE_NET_ERR
    text = result.text
    data = json.loads(text)
    # print(data)

    list = data['list']
    size = len(list)
    for i in range(size):
        item = list[i]
        # print(item)

        theme_name = item['theme_name']
        visit = item['visit']
        post_num = item['post_num']
        is_sub = item['is_sub']
        today_topic_num = item['today_topic_num']
        sub_number = item['sub_number']
        theme_id = item['theme_id']

        theme_id_list.append(theme_id)

        print("id:%d，name:%s, post_num:%d, sub_num:%d" % (theme_id, theme_name, post_num, sub_number))
    saveClassifyConfig(list)


# 全量更新数据
def get_full_datas():
    '''
    id:473，name:社会新鲜事, post_num:82621, sub_num:123738
    id:124，name:萌宠, post_num:67164, sub_num:383310
    id:58191，name:搞笑视频, post_num:518174, sub_num:59565
    id:60369，name:女神萌妹, post_num:53493, sub_num:38431
    id:60660，name:贤人诗社, post_num:9868, sub_num:6212
    id:407，name:影视分享, post_num:115195, sub_num:340420
    id:8466，name:知识分享, post_num:25010, sub_num:33854
    id:63674，name:原创段子手, post_num:107961, sub_num:7724
    id:60386，name:吃鸡, post_num:12095, sub_num:20374
    id:58854，name:牛人集锦, post_num:23955, sub_num:29526
    id:58240，name:搞笑图片, post_num:311610, sub_num:49398
    id:58091，name:汽车, post_num:8086, sub_num:11700
    id:56781，name:情感社区, post_num:67123, sub_num:21635
    id:53647，name:创意脑洞, post_num:13564, sub_num:6562
    id:44289，name:互动区, post_num:42273, sub_num:14274
    id:22871，name:音乐汇, post_num:21082, sub_num:51931
    id:17083，name:Gif专区, post_num:180768, sub_num:26369
    id:164，name:游戏, post_num:25774, sub_num:135328
    id:123，name:美食频道, post_num:28820, sub_num:398578
    '''

    type = TYPE_HOT

    for theme_id in theme_id_list:
        uptime = ""
        retry_count = 0
        while True:
            wait_time = random.randint(5, 6)
            time.sleep(wait_time)

            state, uptime = inner_get_theme_content(theme_id, type, uptime)

            if state == STATE_NO_CONTENT:
                print("当前theme没有内容了,theme_id：%d" % theme_id)
                break
            elif state == STATE_OK:
                pass
            elif state == STATE_NET_ERR:
                print("网络错误，重试，重试次数:%d， theme_id：%d" % (retry_count, theme_id))
                retry_count += 1
                pass
            elif state == STATE_UNKNOWN_ERR:
                print("未知错误，重试，重试次数:%d， theme_id：%d" % (retry_count, theme_id))
                retry_count += 1
                pass

            if retry_count > 10:
                print("已达最大重试次数，中断当前获取,theme_id：%d" % theme_id)
                break


# 增量更新数据,会不停执行
def get_incremental_datas():
    type = TYPE_HOT

    while True:
        pre_time = time.time()
        print("开始一次增量更新，当前时间：%s" % timestamp2Str(time.time()))

        init_update_count_map()

        for theme_id in theme_id_list:
            print("获取theme：%d的数据：" % theme_id)
            uptime = ""
            retry_count = 0
            while True:
                wait_time = random.randint(5, 6)
                time.sleep(wait_time)

                state, uptime, is_all_repeat = inner_get_theme_content(theme_id, type, uptime)

                if state == STATE_OK:
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
                elif state == STATE_UNKNOWN_ERR:
                    print("未知错误，重试，重试次数：%d， type：%s" % (retry_count, type))
                    retry_count += 1

                    time.sleep(3)
                    pass

                # 超过最大重试次数，中断当前类型请求
                if retry_count > MAX_RETRY_COUNT:
                    print("超过最大重试次数：%d，中断当前获取,type：%s" % (retry_count, type))
                    break

        cost_time = time.time() - pre_time
        sleep_time = SLEEP_TIME
        print("完成一次增量更新，耗时:%d秒，当前时间:%s，休眠%d秒" % (cost_time, timestamp2Str(time.time()), sleep_time))

        print_update_count_map()

        # 增量更新一次之后，休息一段时间，下次再更新
        time.sleep(sleep_time)


def inner_get_theme_content(theme_id, type, uptime=""):
    try:

        if uptime == "":
            uptime = "0"
        str_page_range = str.format("%s-%d" % (uptime, 20))
        type_str = "new"
        if type == TYPE_NEW:
            type_str = "new"
        elif type == TYPE_JINGXUAN:
            type_str = "jingxuan"
        elif type == TYPE_HOT:
            type_str = "hot"
        theme_url = str.format("http://d.api.budejie.com/topic/forum/%d/1/%s/budejie-android-6.9.3/%s.json" % (
            theme_id, type_str, str_page_range))
        print("theme_url : %s" % theme_url)

        result = doRequest(theme_url)
        if result == None:
            return STATE_NET_ERR, uptime, False
        text = result.text
        data = None
        try:
            data = json.loads(text)
        except NotFoundException as e:
            print(e)
            return STATE_UNKNOWN_ERR, uptime, False

        # print(data)

        if data == None:
            return STATE_NET_ERR, uptime, False

        count = data['info']['count']
        new_uptime = data['info']['np']

        list = data['list']
        size = len(list)
        if size == 0:
            return STATE_NO_CONTENT, uptime, False

        joke_list = []

        print("theme_id:%d，count:%d, new_update_time:%d" % (theme_id, count, new_uptime))
        for i in range(size):
            item = list[i]
            # print(item)

            id = item['id']
            type = item['type']
            text = item['text']

            user = {}
            if "u" in item:
                user = item['u']

            cate = item['cate']
            comment = item['comment']
            up = item['up']
            down = item['down']
            forward = item['forward']

            passtime = item['passtime']

            obj_url = ""
            download_url = ""
            thumb_url = ""
            width = 0
            height = 0
            duration = 0
            topcomments = ""

            # print("=====id:%s，type:%s, cate:%s, comment:%d, up:%d, down:%d, forward:%d, passtime:%s" % (id, type, cate, int(comment), int(up), down, forward, passtime))

            if type == "text":
                # print("text--text:%s" % (text))
                pass

            elif type == "image":
                image = item['image']

                obj_url = image['big'][0]
                if len(image['big']) > 2:
                    obj_url = image['big'][2]

                download_url = image['download_url'][0]
                if len(image['download_url']) > 2:
                    download_url = image['download_url'][2]

                thumb_url = image['thumbnail_small'][0]

                width = image['width']
                height = image['height']

                # print("image--text%s, obj_url:%s, download_url:%s, thumb_url:%s, width:%d, height:%d" % (text, obj_url, download_url, thumb_url, width, height))
                pass

            elif type == "gif":
                gif = item['gif']

                obj_url = gif['images'][0]
                if len(gif['images']) > 2:
                    obj_url = gif['images'][2]

                download_url = gif['download_url'][0]
                if len(gif['download_url']) > 2:
                    download_url = gif['download_url'][2]

                thumb_url = gif['gif_thumbnail'][0]

                width = gif['width']
                height = gif['height']

                # print("gif--text:%s, obj_url:%s, download_url:%s, thumb_url:%s, width:%d, height:%d" % (text, obj_url, download_url, thumb_url, width, height))
                pass

            elif type == "video":
                video = item['video']

                obj_url = video['video'][0]
                obj_url = obj_url.replace("tvideo.spriteapp.cn", "uvideo.spriteapp.cn")
                obj_url = obj_url.replace("wvideo.spriteapp.cn", "uvideo.spriteapp.cn")

                download_url = video['download'][0]
                download_url = download_url.replace("tvideo.spriteapp.cn", "uvideo.spriteapp.cn")
                download_url = download_url.replace("wvideo.spriteapp.cn", "uvideo.spriteapp.cn")

                thumb_url = video['thumbnail'][0]

                duration = video['duration']
                width = video['width']
                height = video['height']
                playcount = video['playcount']
                playfcount = video['playfcount']

                # print("video--text:%s, obj_url:%s, download_url:%s, thumb_url:%s, duration:%d, width:%d, height:%d, playcount:%d, playfcount:%d" % (text, obj_url, download_url, thumb_url, duration, width, height, playcount, playfcount))
                pass

            if 'top_comments' in item:
                top_comments = item['top_comments']
                comments = []
                for i in range(len(top_comments)):
                    content = top_comments[i]["content"]
                    uid = top_comments[i]['u']["uid"]
                    name = top_comments[i]['u']["name"]
                    head = top_comments[i]['u']["header"][0]
                    # topcomments = topcomments + content
                    # if i < len(top_comments) - 1:
                    #     topcomments = topcomments + SPLIT_STR
                    # print("         topcomment:%s" % (content))
                    comments.append({"content": content, "uid": uid, "name": name, "head": head})
                topcomments = json.dumps(comments, ensure_ascii=False)

            joke_info = {}
            joke_info["id_from_src"] = id
            joke_info["theme_id"] = theme_id
            joke_info["type"] = type
            joke_info["text"] = text
            if len(user) > 0:
                joke_info["user_id"] = user["uid"]
                joke_info["user_name"] = user['name']
                joke_info["user_head"] = user['header'][0]
            else:
                joke_info["user_id"] = ""
                joke_info["user_name"] = ""
                joke_info["user_head"] = ""
            joke_info["src"] = "baisi"
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

        try:
            open_db()

            for joke in joke_list:
                has_joke = False
                if CHECK_RECORD:
                    has_joke = check_has_joke(joke['id_from_src'])
                if not has_joke:
                    # 插入信息到数据库
                    insert_joke(joke)

                    print("插入新记录, id_from_src:%s" % joke['id_from_src'])
                    is_all_repeat = False

                    save_update_count_map(theme_id, 1)
                    success_count += 1

                else:
                    print("已经存在记录, id_from_src:%s" % joke['id_from_src'])

        finally:
            close_db()

        saveThemeConfig(theme_id, success_count, new_uptime)

        return STATE_OK, new_uptime, is_all_repeat

    except Exception as e:
        print("当前更新出错：", e)

    return STATE_UNKNOWN_ERR, uptime, False


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


def saveClassifyConfig(classify_list):
    for item in classify_list:
        theme_id = str(item['theme_id'])
        theme_name = item['theme_name']

        if ini.has_section(theme_id):
            continue
        else:
            ini.add_section(theme_id)

        ini.set_item(theme_id, "theme_id", theme_id)
        ini.set_item(theme_id, "theme_name", theme_name)
        ini.set_item(theme_id, "fetch_times", "0")
        ini.set_item(theme_id, "fetch_num", "0")
        ini.set_item(theme_id, "update_time", "0")
    ini.save()


def saveThemeConfig(theme_id, num, updtime):
    theme_id = str(theme_id)

    fetch_times = int(ini.get_item(theme_id, "fetch_times"))
    fetch_times += 1
    fetch_num = int(ini.get_item(theme_id, "fetch_num"))
    fetch_num += num

    ini.set_item(theme_id, "fetch_times", str(fetch_times))
    ini.set_item(theme_id, "fetch_num", str(fetch_num))
    ini.set_item(theme_id, "update_time", str(updtime))
    ini.save()


def getConfigItem(key):
    return ini.get_item('baisi', key)


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
    global theme_update_count_map
    theme_update_count_map = {}


def save_update_count_map(theme_id, update_count):
    theme_id = str(theme_id)
    if update_count <= 0:
        return
    if not theme_id in theme_update_count_map:
        theme_update_count_map[theme_id] = 0
    pre_count = theme_update_count_map[theme_id]
    theme_update_count_map[theme_id] = pre_count + update_count


def print_update_count_map():
    total_count = 0
    for (theme_id, count) in theme_update_count_map.items():
        print("更新theme_id：%s，更新数量：%d" % (theme_id, count))
        total_count += count
    print("更新总数量：%d" % (total_count))


if __name__ == "__main__":
    loadConfig()

    try:
        open_db()

        get_classify()
        # get_full_datas()
        get_incremental_datas()
    except Exception as e:
        print(e)
    finally:
        close_db()
