"""
__init__.py 用于告诉 Python 这个文件夹是一个 Python 的包
"""
import sys
import os

def import_project(path):
    sys.path.insert(0, os.path.dirname(path))
    project = __import__(os.path.basename(path))
    sys.path.remove(os.path.dirname(path))
    globals()[os.path.basename(path)] = project
    return project
