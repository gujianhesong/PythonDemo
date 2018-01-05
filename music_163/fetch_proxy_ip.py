
import requests
from bs4 import BeautifulSoup
import random

proxies = []
index = -1

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

def getProxyIp():

    srcProxys = []
    destProxys = []

    for index in range(0, 1):
        src_url = 'http://www.xicidaili.com/nt/'
        url = src_url + str(index)
        if index == 0:
            url = src_url

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        ips = soup.findAll('tr')
        for x in  range(1, len(ips)):
            tds = ips[x].findAll('td')
            ip_temp = 'http://' + tds[1].contents[0] + ':' + tds[2].contents[0]

            print('发现ip：%s，检查是否可用。。。' % ip_temp)

            srcProxys.append(ip_temp)
            if validateIp(ip_temp):
                print('可用')
                destProxys.append(ip_temp)
            else:
                print('不可用')

            if(len(destProxys) >= 10):
                break

            # if(str(tds[5].contents[0]) == "HTTP"):
                # if validateIp(ip_temp):
                # destProxys.append(ip_temp)

    print(srcProxys)
    print(destProxys)

    return destProxys


def validateIp(proxy):
    proxy_temp = {"http": proxy}
    url = "http://ip.chinaz.com/getip.aspx"
    try:
        response = requests.get(url, proxies=proxy_temp, timeout=5)
        return True
    except Exception as e:
        return False



if __name__ == '__main_':
    proxys = getProxyIp()
