# -*- coding: utf-8 -*-
import os
import json
import requests
import time
from multiprocessing import Pool


def get_info():
    """ 获取所有图片组的信息 """
    res = []
    with open('pictures/info.txt', 'r') as f:
        for line in f:
            data = json.loads(line)

            for item in data:
                res.append((item[0], item[1], item[2]))
    return res


def download(imgs, processes=10):
    """ 并发下载所有图片 """
    start_time = time.time()
    pool = Pool(processes)
    for img in imgs:
        pool.apply_async(download_one, (img,))

    pool.close()
    pool.join()
    end_time = time.time()
    print('下载完毕,用时:%s秒' % (end_time - start_time))


def download_one(img):
    """ 下载一张图片 """
    url, directory, filepath = img
    # 如果文件已经存在，放弃下载
    if os.path.exists(filepath):
        print('exists:', filepath)
        return

    print('开始下载：%s, %s' % (url, directory))

    setup_download_dir(directory)
    rsp = requests.get(url)
    if rsp.ok:
        print('start download', url)
        with open(filepath, 'wb') as f:
            f.write(rsp.content)
            print('end download', url)

        print('下载完成：%s, %s' % (url, directory))
    else:
        print('下载失败：%s, %s' % (url, directory))


def setup_download_dir(directory):
    """ 设置文件夹，文件夹名为传入的 directory 参数，若不存在会自动创建 """
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as e:
            pass
    return True


if __name__ == "__main__":
    info = get_info()
    download(info, processes=10)
