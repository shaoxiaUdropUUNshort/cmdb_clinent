#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "nothing"
# Date: 2019/5/20


# 1. 安装 saltstack

# ######################远程服务器执行命令############################

import subprocess

result = subprocess.getoutput("salt 'c1.com' cmd.run")
















