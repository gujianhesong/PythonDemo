"""
google翻译，翻译string.xml文件
"""

from GoogleFreeTrans import Translator
import xml.dom.minidom
import os


# 翻译strings文件
def translateStringsMany():
    # languages = ['ko', 'es', 'ru']
    # languages = ['ja', 'ko', 'es', 'ru']
    # languages = ['da', 'de', 'fi', 'vi', 'sk', 'nl', 'pl', 'ro', 'fr', 'cs', 'ms', 'it']
    # languages = ['fi', 'vi', 'sk', 'nl', 'pl', 'ro', 'fr', 'cs', 'ms', 'it']
    languages = ['pt', 'hu', 'sv', 'iw', 'th', 'hi', 'ar']
    for item in languages:
        translateStrings(item)


# 翻译strings文件为特定语言版本，并生成文件
def translateStrings(lan):
    try:
        destDir = 'res2/values-' + lan
        if checkDir(destDir) == False:
            return
        destFile = destDir + '/README.md'

        print(destFile)

        content = ""
        with open('res2/values/README.md', 'r', encoding='utf-8') as f:
            for line in f:
                print(line)
                line = translate(line, lan)
                print(line)
                content += line + '\n'

        with open(destFile, 'w', encoding='utf-8') as f:
            f.write(content)

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
