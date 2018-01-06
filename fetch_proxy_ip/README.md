>转载请标明出处： 
<br>http://blog.csdn.net/hesong1120/article/details/78990975
<br>本文出自:[hesong的专栏](http://blog.csdn.net/hesong1120?ref=toolbar)

## 前言
使用爬虫爬取网站的信息常常会遇到的问题是，你的爬虫行为被对方识别了，对方把你的IP屏蔽了，返回不了正常的数据给你。那么这时候就需要使用代理服务器IP来伪装你的请求了。
免费代理服务器网站有：
- [西刺免费代理IP](http://www.xicidaili.com/)
- [快代理](https://www.kuaidaili.com/free/inha/)
- [66免费代理](http://www.66ip.cn/index.html)

下面我们以[西刺免费代理IP](http://www.xicidaili.com/)为例子看看是如何获取可用IP的。主要分为以下几个步骤：
1. 请求url，获取网页数据
2. 解析网页数据，找到包含【IP地址】和【端口】信息的节点，解析出这两个数据
3. 验证取得的【IP地址】和【端口】信息是否可用
4. 将验证可用的【IP地址】和【端口】信息保存起来（暂存到列表，或保存到文件，保存到数据库）

### 1. 请求网页数据
请求网页数据是使用requests库去做网络请求的，填入url，和header头部信息，使用get请求方式去请求，得到response相应后，返回response.text即是响应的文本内容，即网页文本内容。

```
# 请求url，获取网页数据
def _requestUrl(index):
    src_url = 'http://www.xicidaili.com/nt/'
    url = src_url + str(index)
    if index == 0:
        url = src_url

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    }
    response = requests.get(url, headers=headers)
    return response.text
```

用浏览器打开网址看一下
![python获取代理服务器ip](https://raw.githubusercontent.com/gujianhesong/PythonDemo/master/fetch_proxy_ip/screenshot/python%E8%8E%B7%E5%8F%96%E4%BB%A3%E7%90%86ip_1.jpg)

### 2. 解析网页数据
返回正确的网页数据之后，就可以开始对它进行解析了，这里使用BeautifulSoup库进行网页内容解析。如果是Chrome浏览器，按f12可以查看网页源码，如图
![python获取代理服务器ip](https://raw.githubusercontent.com/gujianhesong/PythonDemo/master/fetch_proxy_ip/screenshot/python%E8%8E%B7%E5%8F%96%E4%BB%A3%E7%90%86ip_2.jpg)
找到某个tr行，第1个和第2个td列就是是ip和端口信息，因此我们可以用BeautifulSoup查找所以的tr行，再查找该tr行的第1个和第2个td列即可以获取该页面上所有的ip和端口信息了。

```
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
```

### 3. 验证IP和端口是否可用
解析到页面上的所有ip和端口信息后，还需要验证它是否是有效的，然后对它们进行过滤，获取有效的ip列表。验证方法就是使用它作为代理地址，去请求网络，看是否能请求成功，如果请求成功，说明是有效的。当然，这里需要加上超时时间，以避免等待时间过长，这里设置超时时间为5秒。
```
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

# 验证ip是否有效
def validateIp(proxy):
    proxy_temp = {"http": proxy}
    url = "http://ip.chinaz.com/getip.aspx"
    try:
        response = requests.get(url, proxies=proxy_temp, timeout=5)
        return True
    except Exception as e:
        return False
```

### 4. 发起请求，保存可用IP和端口信息
接下来要开始调用以上代码了。这里只爬取第1页数据
```
# 获取可用的代理ip列表
def getProxyIp():

    allProxys = []

    startPage = 0
    endPage = 1

    for index in range(startPage, endPage):
        print('查找第 %s 页的ip信息' % index)

        # 请求url，获取网页数据
        content = _requestUrl(index)
        # 解析网页数据，获取ip和端口信息
        list = parseProxyIpList(content)
        # 过滤有效的ip信息
        list = filterValidProxyIp(list)
        # 添加到有效列表中
        allProxys.append(list)

        print('第 %s 页的有效ip有以下：' % index)
        print(list)

    print('总共找到有效ip有以下：')
    print(allProxys)

    return allProxys

```
运行该爬虫程序之后，就可以开始爬取代理服务器信息了。如图

![python获取代理服务器ip](https://raw.githubusercontent.com/gujianhesong/PythonDemo/master/fetch_proxy_ip/screenshot/python%E8%8E%B7%E5%8F%96%E4%BB%A3%E7%90%86ip_3.jpg)
![python获取代理服务器ip](https://raw.githubusercontent.com/gujianhesong/PythonDemo/master/fetch_proxy_ip/screenshot/python%E8%8E%B7%E5%8F%96%E4%BB%A3%E7%90%86ip_4.jpg)
![python获取代理服务器ip](https://raw.githubusercontent.com/gujianhesong/PythonDemo/master/fetch_proxy_ip/screenshot/python%E8%8E%B7%E5%8F%96%E4%BB%A3%E7%90%86ip_5.jpg)

## 总结
通过以上步骤就可以获取有效的代理服务器IP信息了，其他代理服务器IP网站的获取方式和这个大同小异，主要在于解析网页数据那里，需要找到包含IP和端口数据的标签，然后解析获取到。有了代理服务器IP，你就可以爬取更多网站的信息了。

还有个问题是，网站可能会对某个IP检测，如果超过一定请求次数，就会对其进行屏蔽，那这样会导致程序中断，无法获取所有的信息，这如何解决呢？欢迎关注我的微信公众号hesong，了解具体应对方式。

附上[源码地址](https://github.com/gujianhesong/PythonDemo/tree/master/fetch_proxy_ip)

>[我的博客](http://blog.csdn.net/hesong1120?ref=toolbar)
<br>[GitHub](https://github.com/gujianhesong)
<br>[我的简书](https://www.jianshu.com/u/75d212bdd107)
<br>群号：<font color=#ff0000 size=3>194118438</font>，欢迎入群
<br>微信公众号 **hesong** ，微信扫一扫下方二维码即可关注：
<br>![](https://raw.githubusercontent.com/gujianhesong/hesong/master/%E5%BE%AE%E4%BF%A1%E5%85%AC%E4%BC%97%E5%8F%B7.jpg)