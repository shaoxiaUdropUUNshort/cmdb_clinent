#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "nothing"
# Date: 2019/5/20


# Agent形式

# 1. 采集资产
# 2. 将资产发送到API


######SSH形式
# 1. 获取今日未采集主机列表
# 2.采集资产
# 3. 将资产数据发送到API


##### Salt
# 1. 获取今日未采集主机列表
# 2.采集资产
# 3. 将资产数据发送到API
import os
import json
import time
import hashlib
import requests
from src import plugins
from lib.serialize import Json
from lib.log import Logger
from conf import settings
from concurrent.futures import ThreadPoolExecutor


class AutoBase(object):
    def __init__(self):
        self.asset_api = settings.ASSET_API  # "http://127.0.0.1:8000/api/asset"
        self.key = settings.KEY  # # 用于API认证的KEY '299095cc-1330-11e5-b06a-a45e60bec08b'
        self.key_name = settings.AUTH_KEY_NAME   ## 用于API认证的请求头 'auth-key'

    def auth_key(self):
        '''接口认证'''
        ha = hashlib.md5()  # 可加盐
        time_span = time.time()
        ha.update(bytes("%s|%f" % (self.key, time_span), encoding='utf-8'))
        encryption = ha.hexdigest()
        result = "%s|%f" % (encryption, time_span)
        return {self.key_name: result}

    def get_asset(self):
        '''
        get方式获取，未采集的资产. ssh 和 salt 方式
        :return: {"data": [{"hostname": "c1.com"}, {"hostname": "c2.com"}], "error": null, "message": null, "status": true}
        '''
        try:
            headers = {}
            headers.update(self.auth_key())
            response = requests.get(
                url=self.asset_api,
                headers=headers
            )
        except Exception as e:
            response = e
        return response.json()

    def post_asset(self, msg, callback=None):
        '''
        post 方式向接口提交资产信息
        :param msg:
        :param callback:
        :return:
        '''
        status = True
        try:
            headers = {}
            headers.update(self.auth_key())
            response = requests.post(
                url=self.asset_api,
                headers=headers,
                json=msg
            )
            print(headers)
        except Exception as e:
            response = e
            status = False
        if callback:
            callback(status, response)

    def process(self):
        """
        派生类需要继承此方法，用于处理请求的入口
        :return:
        """
        raise NotImplementedError('you must implement process method')

    def callback(self, status, response):
        """
        提交资产后的回调函数
        :param status: 是否请求成功
        :param response: 请求成功，则是响应内容对象；请求错误，则是异常对象
        :return:
        """
        if not status:
            Logger().log(str(response), False)
            return
        ret = json.loads(response.text)
        if ret['code'] == 1000:
            Logger().log(ret['message'], True)
        else:
            Logger().log(ret['message'], False)


class AutoAgent(AutoBase):
    def __init__(self):
        self.cert_file_path = settings.CERT_FILE_PATH
        # 这个是保存着 每一个主机名的文件。 主机名保证唯一。
        super(AutoAgent, self).__init__()  # 直接继承父类的初始化方法

    def load_local_cert(self):
        """
        获取存储在本地以为标识
        :return:
        """
        if not os.path.exists(self.cert_file_path):  # 判断当前的路径是否是一个真实的路径。
            return None
        with open(self.cert_file_path, mode='r') as f:
            data = f.read()  # 读取到所有的主机名
        if not data:
            return None
        cert = data.strip()
        return cert

    def write_local_cert(self, cert):
        """
        写入本地以为标识, 一般这件事。在第一次装机时，就会完成。后续一般用不到
        :param cert:
        :return:
        """
        if not os.path.exists(self.cert_file_path):
            os.makedirs(os.path.basename(self.cert_file_path))
        with open(settings.CERT_FILE_PATH, mode='w') as f:
            f.write(cert)

    def process(self):
        server_info = plugins.get_server_info()   # 这里server_info是一个对象 BaseResponse的实例 对象。
        # print(server_info.data)
        # print(type(server_info.data))
        if not server_info.status:
            # 如果这个值为  false 说明，发成了错误。那就直接返回。不再进行下一步的操作
            return
        local_cert = self.load_local_cert()  # 获取到所有的主机名
        if local_cert:
            if local_cert == server_info.data['hostname']:
                pass
            else:
                server_info.data['hostname'] = local_cert
                # 如果不相等将本地保存的 主机名赋值给他。保证后端接收到的是，这个唯一的主机名
        else:
            self.write_local_cert(server_info.data['hostname'])  # 如果当前文件中没有主机名，就写入

        server_json = Json.dumps(server_info.data)  # 使用自定制的 序列化工具，将对象序列化。
        self.post_asset(server_json, self.callback)  # 使用父类的方法。发送所有的数据。


class AutoSSH(AutoBase):
    def process(self):
        """
        根据主机名获取资产信息，将其发送到API
        :return:
        """
        task = self.get_asset()
        if not task['status']:
            Logger().log(task['message'], False)

        pool = ThreadPoolExecutor(10)   # 开10个线程
        for item in task['data']:
            hostname = item['hostname']
            pool.submit(self.run, hostname)
        pool.shutdown(wait=True)

    def run(self, hostname):
        server_info = plugins.get_server_info(hostname)
        server_json = Json.dumps(server_info.data)
        self.post_asset(server_json, self.callback)


class AutoSalt(AutoBase):
    def process(self):
        """
        根据主机名获取资产信息，将其发送到API
        :return:
        {
            "data": [ {"hostname": "c1.com"}, {"hostname": "c2.com"}],
           "error": null,
           "message": null,
           "status": true
        }
        """
        task = self.get_asset()
        if not task['status']:
            Logger().log(task['message'], False)

        # 创建线程池：最大可用线程10
        pool = ThreadPoolExecutor(10)
        # "data": [ {"hostname": "c1.com"}, {"hostname": "c2.com"}],
        for item in task['data']:
            # c1.com  c2.com
            hostname = item['hostname']
            pool.submit(self.run, hostname)
            # run(c1.com) 1
            # run(c2.com) 2
        pool.shutdown(wait=True)

    def run(self, hostname):
        # 获取指定主机名的资产信息  server_info.data 中的信息。就是以下的内容
        # {'status': True, 'message': None, 'error': None,
        # 'data': {'disk': <lib.response.BaseResponse object at 0x00000000014686A0>,
        # 'main_board': <lib.response.BaseResponse object at 0x00000000014689B0>,
        # 'nic': <lib.response.BaseResponse object at 0x0000000001478278>,
        # 'memory': <lib.response.BaseResponse object at 0x0000000001468F98>,
        # 'os_platform': 'linux', 'os_version': 'CentOS release 6.6 (Final)', 'hostname': 'c1.com',
        # 'cpu': <lib.response.BaseResponse object at 0x0000000001468E10>}}

        server_info = plugins.get_server_info(hostname)
        # 序列化成字符串
        server_json = Json.dumps(server_info.data)
        # 发送到API
        self.post_asset(server_json, self.callback)





