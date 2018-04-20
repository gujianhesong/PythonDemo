"""
google翻译，翻译string.xml文件
"""

from GoogleFreeTrans import Translator
import xml.dom.minidom
import os


# 翻译strings文件
def translateStringsMany():
    languages = ['it']
    # languages = ['ja', 'ko', 'es', 'ru']
    # languages = ['da', 'de', 'fi', 'vi', 'sk', 'nl', 'pl', 'ro', 'fr', 'cs', 'ms', 'it']
    # languages = ['pt', 'hu', 'sv', 'iw', 'th', 'hi', 'ar']
    for item in languages:
        translateStrings(item)


# 翻译strings文件为特定语言版本，并生成文件
def translateStrings(lan):
    try:
        dom = xml.dom.minidom.parse('res/values/strings.xml')
        root = dom.documentElement
        # print(root.nodeName)
        # print(root.nodeValue)
        # print(root.nodeType)

        destDir = 'res/values-' + lan
        if checkDir(destDir) == False:
            return
        destFile = destDir + '/strings.xml'

        print(destFile)

        childs = root.getElementsByTagName('string')
        print(childs)

        for child in childs:
            try:
                name = child.getAttribute('name')
                value = child.firstChild.data

                print("src   %s : %s" % (name, value))

                value = transWithSplit(value, lan)

                child.firstChild.data = value

                print("dest   %s : %s" % (name, value))
            except Exception as err:
                print(err)

        with open(destFile, 'w', encoding='utf-8') as f:
            f.write(dom.toprettyxml(newl=""))

    except Exception as err:
        print(err)


# 可以翻译字符串，并且可以处理其中\n, '的问题
def transWithSplit(value, lan):
    value = value.replace('\\n', '\n')

    newValue = ''
    try:
        if (value.index('\n') >= 0):

            arr = value.split('\n')
            index = 0
            for str in arr:
                newValue += translate(str, lan)
                if (index < len(arr)):
                    newValue += '\\n'
                index = index + 1
            print('newValue : ' + newValue)
    except Exception as err:
        newValue = translate(value, lan)
        print('newValue : ' + newValue)

    newValue = newValue.replace('\'', '\\\'')

    return newValue


# 翻译字符串
def translate(str, lan):
    # translator = Translator.translator(src='en', dest='zh-CN')
    translator = Translator.translator(src='en', dest=lan)
    result = translator.translate(str)
    # print(result)
    return result


# 检查目录是否存在，没有则创建
def checkDir(directory):
    """ 设置文件夹，文件夹名为传入的 directory 参数，若不存在会自动创建 """
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as e:
            return False
    return True


if __name__ == '__main__':
    translateStringsMany()
    #
    # languages = ['ja', 'ko', 'es', 'ru', 'zh-TW']
    # for item in languages:
    #     transWithSplit('adjust', item)
    #
    # value = 'Alpha'
    # transWithSplit(value, 'zh-TW')
