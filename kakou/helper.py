# -*- coding: utf-8 -*-
import os

def make_dirs(path):
    """创建文件夹"""
    try:
        if os.path.isdir(path):
            pass
        else:
            os.makedirs(path)
    except IOError,e:
        raise
