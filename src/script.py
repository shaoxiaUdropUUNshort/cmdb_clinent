#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "nothing"
# Date: 2019/5/20

import subprocess
from src.client import AutoAgent
from src.client import AutoSSH
from src.client import AutoSalt
from conf import settings


# 这里来确定 当前的模式是什么。 从而判断出， 要实例化出那种对象来 进行数据的采集。

def client():
    if settings.MODE == "Agent":
        cli = AutoAgent()  # 直接使用subprocess   subprocess.getoutput(命令) 拿到数据
    elif settings.MODE == "SSH":
        cli = AutoSSH()  # 使用 paramiko
    elif settings.MODE == "Salt":
        cli = AutoSalt()  # 使用 salt 模块
    else:
        raise Exception("请配置采集模式，如：ssh,agent,salt")
    cli.process()











