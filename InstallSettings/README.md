>转载请标明出处： 
<br>http://blog.csdn.net/hesong1120/article/details/78988597
<br>本文出自:[hesong的专栏](http://blog.csdn.net/hesong1120?ref=toolbar)

## 前言

>工欲善其事必先利其器

Python开发的第一步就是开发环境的搭建配置了，一个清晰流畅并且简单的配置过程会让我们在Python的学习之路开个好头，你会更有信心使用它的。
**注意，本篇虽然是介绍Python3的环境配置，不过Python2的配置大同小异，流程是一样的**。Python开发环境搭建个人熟悉的有两种：
1. **正常安装模式：Python安装 + PyCharm安装 + 项目导所需库**
2. **简易安装模式：Anaconda安装 + PyCharm安装 + 项目导个别所需库（个别Anaconda不包含的）**

下面说说这两种安装模式的优缺点：
> - 正常安装模式
<br>优点：让你更加清晰环境配置的过程，全程充满操作感~
<br>缺点：相应的，操作较麻烦，初学者可能会不知所措

> - 简易安装模式
<br>优点：配置简单，轻松上手，已集成大部分常用库，无需自己导入
<br>缺点：配置简单导致不清楚它的配置原理，没有操作爽快感~

接下来我们按这两种方式介绍安装配置过程

## 正常安装模式
正常安装模式需要进行几个步骤，以得到一个可用的开发环境。
1. 下载安装Python
2. 下载安装PyCharm
3. 打开PyCharm，新建项目
4. 项目导包

#### 1. 下载安装Python
这里是[Python官方下载地址](https://www.python.org/downloads/)，分为Python3.6和Python2.7两个版本，自己选择对应的版本下载安装。安装完之后，需要配置环境变量（以WIN7，WIN10为例）：
1. 右键【我的电脑】，选择【属性】
2. 找到点击左侧的【高级系统设置】，打开了【系统属性】界面
3. 点击【环境变量】，打开了【环境变量】界面
4. 找到下方【系统变量】的【Path】，点击【编辑】
5. 找到Python的安装目录，比如我的【C:\Program Files (x86)\Python\Python36】
6. 添加【C:\Program Files (x86)\Python\Python36】和【C:\Program Files (x86)\Python\Python36\Script】到Path中，点击保存
7. 打开CMD命令行，输入python测试是否配置成功
![python环境配置](https://raw.githubusercontent.com/gujianhesong/PythonDemo/master/InstallSettings/normal/python%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE1.png)
![python环境配置](https://raw.githubusercontent.com/gujianhesong/PythonDemo/master/InstallSettings/normal/python%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE2.jpg)

#### 2. <span id="jump">下载安装PyCharm</span>

这里是[PyCharm官方下载地址](https://www.jetbrains.com/zh/pycharm/specials/pycharm/pycharm.html?utm_source=baidu&utm_medium=cpc&utm_campaign=cn-bai-br-pycharm-ex-pc&utm_content=pycharm-download&utm_term=pycharm%20%E4%B8%8B%E8%BD%BD)，下载安装即可

#### 3. PyCharm新建项目
打开PyCharm，选择【New Project】，点【Create】创建

![PyCharm新建项目](https://raw.githubusercontent.com/gujianhesong/PythonDemo/master/InstallSettings/normal/PyCharm%E6%96%B0%E5%BB%BA%E9%A1%B9%E7%9B%AE1.png)

进入项目，

![PyCharm新建项目](https://raw.githubusercontent.com/gujianhesong/PythonDemo/master/InstallSettings/normal/PyCharm%E6%96%B0%E5%BB%BA%E9%A1%B9%E7%9B%AE2.png)

创建个python文件

![PyCharm新建项目](https://raw.githubusercontent.com/gujianhesong/PythonDemo/master/InstallSettings/normal/PyCharm%E6%96%B0%E5%BB%BA%E9%A1%B9%E7%9B%AE3.png)

![PyCharm新建项目](https://raw.githubusercontent.com/gujianhesong/PythonDemo/master/InstallSettings/normal/PyCharm%E6%96%B0%E5%BB%BA%E9%A1%B9%E7%9B%AE4.png)

![PyCharm新建项目](https://raw.githubusercontent.com/gujianhesong/PythonDemo/master/InstallSettings/normal/PyCharm%E6%96%B0%E5%BB%BA%E9%A1%B9%E7%9B%AE5.png)

#### 4. 项目导包
python文件创建之后试着导入一些包，发现报错，没有找到，【ALT+ENTER】提示安装

![PyCharm新建项目](https://raw.githubusercontent.com/gujianhesong/PythonDemo/master/InstallSettings/normal/PyCharm%E6%96%B0%E5%BB%BA%E9%A1%B9%E7%9B%AE6.jpg)

安装完成后，错误消失

![PyCharm新建项目](https://raw.githubusercontent.com/gujianhesong/PythonDemo/master/InstallSettings/normal/PyCharm%E6%96%B0%E5%BB%BA%E9%A1%B9%E7%9B%AE7.jpg)

到这里正常安装配置就完成了，可以开心的码代码了！

## 简易安装模式
简易安装模式就很简单了，分为以下步骤：
1. 下载安装Anaconda
2. 下载安装PyCharm
3. 打开PyCharm，新建项目
4. 项目导包（少部分不包含的库）

#### 1. 下载安装Anaconda
这里是[Anaconda官方下载地址](https://www.anaconda.com/download/)，如果速度慢，可以去下载[国内镜像](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/),下载安装，注意，如果之前没有安装Python并配置环境变量的话，可以勾选这两个选项，让Anaconda来配置它内置的Python环境变量，这样就可以直接在命令行使用python命令了，而不需要你手动去配置。

![Anaconda安装](https://raw.githubusercontent.com/gujianhesong/PythonDemo/master/InstallSettings/simple/Anaconda%E5%AE%89%E8%A3%85.png)

#### 2. 下载安装PyCharm
参考正常安装模式的[下载安装PyCharm](#jump)

#### 3. PyCharm新建项目
打开PyCharm，选择【New Project】新建一个项目，注意选择【Existing interpreter】，这样就可以共用已经存在python解释器环境。

![PyCharm新建项目](https://raw.githubusercontent.com/gujianhesong/PythonDemo/master/InstallSettings/simple/PyCharm%E6%96%B0%E5%BB%BA%E9%A1%B9%E7%9B%AE1.jpg)

![PyCharm新建项目](https://raw.githubusercontent.com/gujianhesong/PythonDemo/master/InstallSettings/simple/PyCharm%E6%96%B0%E5%BB%BA%E9%A1%B9%E7%9B%AE2.jpg)

新建一个python文件，导入一些库，你会发现有几个已经存在了，那是因为Anaconda中已经包含了这些库

![PyCharm新建项目](https://raw.githubusercontent.com/gujianhesong/PythonDemo/master/InstallSettings/simple/PyCharm%E6%96%B0%E5%BB%BA%E9%A1%B9%E7%9B%AE3.jpg)

但是还是有少部分库找不到，打开命令行，输入下面的语句，即可安装

![PyCharm新建项目](https://raw.githubusercontent.com/gujianhesong/PythonDemo/master/InstallSettings/simple/PyCharm%E6%96%B0%E5%BB%BA%E9%A1%B9%E7%9B%AE4.jpg)

安装完成后，就可以使用了

![PyCharm新建项目](https://raw.githubusercontent.com/gujianhesong/PythonDemo/master/InstallSettings/simple/PyCharm%E6%96%B0%E5%BB%BA%E9%A1%B9%E7%9B%AE5.jpg)

到这里简易安装配置就完成了，可以开心的码代码啦！

## 总结
上面介绍了正常安装和简易安装方式，其实都是比较简单的，后面就可以开心的进入Python精彩世界了~

>[我的博客](http://blog.csdn.net/hesong1120?ref=toolbar)
<br>[GitHub](https://github.com/gujianhesong)
<br>[我的简书](https://www.jianshu.com/u/75d212bdd107)
<br>群号：<font color=#ff0000 size=3>194118438</font>，欢迎入群
<br>微信公众号 **hesong** ，微信扫一扫下方二维码即可关注：
<br>![](https://raw.githubusercontent.com/gujianhesong/hesong/master/%E5%BE%AE%E4%BF%A1%E5%85%AC%E4%BC%97%E5%8F%B7.jpg)