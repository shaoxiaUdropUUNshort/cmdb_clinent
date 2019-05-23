#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "nothing"
# Date: 2019/5/20

# Agent方式。

import subprocess
import requests
import re

result = subprocess.getoutput('ifconfig')

##########################采集数据##########################
# # 整理资产信息， 对获得result进行正则处理。 存入字典.
date_dict = {
    'nic':{},
}


###########################发送数据##########################
# 发送数据

requests.post('http://...', data=date_dict)

































