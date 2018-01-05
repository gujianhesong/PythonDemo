"""
获取所有的歌手信息
"""
import requests
from bs4 import BeautifulSoup
import sql
import time
import fetch_proxy_ip
import random

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': '_ntes_nnid=7eced19b27ffae35dad3f8f2bf5885cd,1476521011210; _ntes_nuid=7eced19b27ffae35dad3f8f2bf5885cd; usertrack=c+5+hlgB7TgnsAmACnXtAg==; Province=025; City=025; NTES_PASSPORT=6n9ihXhbWKPi8yAqG.i2kETSCRa.ug06Txh8EMrrRsliVQXFV_orx5HffqhQjuGHkNQrLOIRLLotGohL9s10wcYSPiQfI2wiPacKlJ3nYAXgM; P_INFO=hourui93@163.com|1476523293|1|study|11&12|jis&1476511733&mail163#jis&320100#10#0#0|151889&0|g37_client_check&mailsettings&mail163&study&blog|hourui93@163.com; NTES_SESS=Fa2uk.YZsGoj59AgD6tRjTXGaJ8_1_4YvGfXUkS7C1NwtMe.tG1Vzr255TXM6yj2mKqTZzqFtoEKQrgewi9ZK60ylIqq5puaG6QIaNQ7EK5MTcRgHLOhqttDHfaI_vsBzB4bibfamzx1.fhlpqZh_FcnXUYQFw5F5KIBUmGJg7xdasvGf_EgfICWV; S_INFO=1476597594|1|0&80##|hourui93; NETEASE_AUTH_SOURCE=space; NETEASE_AUTH_USERNAME=hourui93; _ga=GA1.2.1405085820.1476521280; JSESSIONID-WYYY=cbd082d2ce2cffbcd5c085d8bf565a95aee3173ddbbb00bfa270950f93f1d8bb4cb55a56a4049fa8c828373f630c78f4a43d6c3d252c4c44f44b098a9434a7d8fc110670a6e1e9af992c78092936b1e19351435ecff76a181993780035547fa5241a5afb96e8c665182d0d5b911663281967d675ff2658015887a94b3ee1575fa1956a5a%3A1476607977016; _iuqxldmzr_=25; __utma=94650624.1038096298.1476521011.1476595468.1476606177.8; __utmb=94650624.20.10.1476606177; __utmc=94650624; __utmz=94650624.1476521011.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'DNT': '1',
    'Host': 'music.163.com',
    'Pragma': 'no-cache',
    'Referer': 'http://music.163.com/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}
proxies = {
    'http': 'http://110.73.3.112:8123',
    'http': 'http://42.245.252.35:80',
    'http': 'http://106.14.51.145:8118',
    'http': 'http://116.199.115.78:80',
    'http': 'http://123.147.165.143:8080',
    'http': 'http://58.62.86.216:9999',
    'http': 'http://202.201.3.121:3128',
    'http': 'http://119.29.201.134:808',
    'http': 'http://61.155.164.112:3128',
    'http': 'http://61.155.164.107:3128',
    'http': 'http://61.135.217.7:80',
    'http': 'http://116.199.115.78:80',
}

def save_artist(group_id, initial):
    proxies = fetch_proxy_ip.getOneAvailableProxy()

    print('请求歌手%s组，%s' % (group_id, initial))

    print('使用ip %s 请求数据' % proxies)

    params = {'id': group_id, 'initial': initial}
    r = None
    try:
        r = requests.get('http://music.163.com/discover/artist/cat', proxies=proxies, headers=headers, params=params, timeout=5)
    except Exception as e:
        print(e)

    if(r == None):
        retryForInvalid(group_id, initial)
        return

    # 网页解析
    soup = BeautifulSoup(r.content.decode(), 'html.parser')
    body = soup.body

    #类别中前10歌手
    hot_artists = body.find_all('a', attrs={'class': 'msk'})
    #类别中非前10歌手
    artists = body.find_all('a', attrs={'class': 'nm nm-icn f-thide s-fc0'})

    if (len(hot_artists) == 0):
        retryForInvalid(group_id, initial)
        return

    for artist in hot_artists:
        artist_id = artist['href'].replace('/artist?id=', '').strip()
        artist_name = artist['title'].replace('的音乐', '')
        print("歌手: %s, %s" % (artist_id, artist_name))

        try:
            sql.insert_artist(artist_id, artist_name)
        except Exception as e:
            # 打印错误日志
            print(e)

    for artist in artists:
        artist_id = artist['href'].replace('/artist?id=', '').strip()
        artist_name = artist['title'].replace('的音乐', '')
        print("歌手: %s, %s" % (artist_id, artist_name))

        try:
            sql.insert_artist(artist_id, artist_name)
        except Exception as e:
            # 打印错误日志
            print(e)

def retryForInvalid(group_id, initial):
    print('该ip不可用，尝试新的ip')
    fetch_proxy_ip.setTheProxyInavalid()
    save_artist(group_id, initial)



# id，1001华语男歌手，1002华语女歌手，1003华语乐队
id = 1001
# initial，65-90代表A-Z，0代表其他
FIRST_INITIAL, LAST_INITIAL = 65, 91
initial = FIRST_INITIAL

#save_artist(id, 0)
for initial in range(FIRST_INITIAL, LAST_INITIAL):
    save_artist(id, initial)
