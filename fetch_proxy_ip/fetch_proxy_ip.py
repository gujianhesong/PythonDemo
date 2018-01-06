
import requests
from bs4 import BeautifulSoup
import random

proxies = []
index = -1

'''

'''
def getOneAvailableProxy():
    global proxies
    if len(proxies) == 0:
        proxies = fetchAvalableProxyIpList()

    global index
    if (index < 0):
        index = random.randint(0, len(proxies) - 1)
    return proxies[index]

def setTheProxyInavalid():
    global index
    index = -1

def fetchAvalableProxyIpList():
    proxies = []
    for proxy in getProxyIp():
        proxies.append({'http': proxy})
    return proxies

# 请求url，获取网页数据
def _requestUrl(index):
    src_url = 'http://www.xicidaili.com/nt/'
    url = src_url + str(index)
    if index == 0:
        url = src_url

    proxies = {
        'http': 'http://110.73.3.112:8123',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    }
    response = requests.get(url, headers=headers)
    return response.text

# 解析网页数据，获取ip和端口信息
def parseProxyIpList(content):
    list = []

    soup = BeautifulSoup(content, 'html.parser')
    ips = soup.findAll('tr')
    for x in range(1, len(ips)):
        tds = ips[x].findAll('td')
        ip_temp = 'http://' + tds[1].contents[0] + ':' + tds[2].contents[0]
        print('发现ip：%s' % ip_temp)
        list.append(ip_temp)
    return list

# 过滤有效的ip信息
def filterValidProxyIp(list):
    print('开始过滤可用ip 。。。')
    validList = []
    for ip in list:
        if validateIp(ip):
            print('%s 可用' % ip)
            validList.append(ip)
        else:
            print('%s 无效' % ip)
    return validList

# 获取可用的代理ip列表
def getProxyIp():

    allProxys = []

    startPage = 0
    endPage = 1

    for index in range(startPage, endPage):
        print('查找第 %s 页的ip信息' % index)

        content = _requestUrl(index)
        list = parseProxyIpList(content)
        list = filterValidProxyIp(list)
        allProxys.append(list)

        print('第 %s 页的有效ip有以下：' % index)
        print(list)

    print('总共找到有效ip有以下：')
    print(allProxys)

    return allProxys

def validateIp(proxy):
    proxy_temp = {"http": proxy}
    url = "http://ip.chinaz.com/getip.aspx"
    try:
        response = requests.get(url, proxies=proxy_temp, timeout=5)
        return True
    except Exception as e:
        return False


if __name__ == '__main__':
    proxies = getProxyIp()
