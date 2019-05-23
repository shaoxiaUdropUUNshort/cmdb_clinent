#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "nothing"
# Date: 2019/5/20

import requests
import paramiko

# ######################获取今日未采集数据 的主机名#########################

# res = requests.get('http://127.0.0.1/assets.html')




# ####################### 通过paramiko 链接远程服务器执行命令

# 创建 SSH 对象
ssh = paramiko.SSHClient()
# 允许链接 不再 know_host 文件中的主机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 链接服务器
ssh.connect(hostname='192.168.1.5', port=22, username='python_web', password='123456')

# 执行命令
stdin, stdout, stderr = ssh.exec_command('df')
# stdin.write('yes')  # 可以在执行命令之后再写入一些东西
# 获取命令的结果

result = stdout.read()

# 关闭链接
ssh.close()


# #################### 发送数据 ####################################
# data_dict = {result}














