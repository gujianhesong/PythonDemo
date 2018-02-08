"""
批量获取图片地址等信息，并存储到文件中
"""
import requests
from bs4 import BeautifulSoup
import os
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
}

save_path = 'pictures'
main_url = 'http://www.mmjpeg.com/meitu/'


def save_pictures_info(id):
    print('开始请求页面id: %s' % (id))
    list = []

    for page in range(1, 20):
        print('开始请求页面id: %s, page: %s' % (id, page))
        # print('使用ip %s 请求数据' % proxies)

        if page == 1:
            url = str('%s%s.html#p' % (main_url, id))
        else:
            url = str('%s%s_%s.html#p' % (main_url, id, page))

        r = None
        try:
            r = requests.get(url, headers=headers, timeout=5)
        except Exception as e:
            print(e)

        text = r.content
        # 网页解析
        soup = BeautifulSoup(text, 'html.parser')

        div = soup.find('div', attrs={'class': 'picsbox picsboxcenter'})

        if (not div):
            break

        img = div.find('img')['lazysrc']
        title = div.find('img')['alt']
        print('url：%s， title：%s' % (img, title))

        directory = os.path.join(save_path, str(id))
        filepath = os.path.join(directory, "%s.jpg" % title)

        list.append((
            img, directory, filepath
        ))

    print('完成请求页面id: %s' % (id))
    print('获取网址信息：%s' % list)
    save_page(list)


def save_page(page_json):
    """ 保存某页面的信息 """
    txt = json.dumps(page_json)

    setup_download_dir(save_path)
    with open(save_path + '/info.txt', 'a') as f:
        f.write(txt)
        f.write('\n')


def setup_download_dir(directory):
    """ 设置文件夹，文件夹名为传入的 directory 参数，若不存在会自动创建 """
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as e:
            pass
    return True


if __name__ == "__main__":
    for id in range(30000, 30030):
        save_pictures_info(id)
