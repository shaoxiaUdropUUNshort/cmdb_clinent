#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "nothing"
# Date: 2019/5/20

import os
import sys
from src.script import client

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
# print(BASEDIR)  # D:\cmdb
# 将自己的当前临时添加到 环境变量中。 当前项目中其他的所有模块在相对的导入的时候，都会根据这个路径来到如

if __name__ == '__main__':
    client()
