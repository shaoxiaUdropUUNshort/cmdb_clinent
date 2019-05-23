#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "nothing"
# Date: 2019/5/20


# from concurrent.futures import ThreadPoolExecutor
# import time
#
# def task(arg):
#     print(arg)
#     time.sleep(1)
#
#
# pool = ThreadPoolExecutor(10)
#
#
# for i in range(50):
#     pool.submit(task, i)


import requests
import hashlib
import time


def auth_key_time(appid):
    current_time = time.time()
    app_id_time = '%s|%s' % (app_id, current_time)
    m = hashlib.md5()
    m.update(bytes(app_id_time, encoding='utf-8'))
    authkey = m.hexdigest()
    authkey_time = '%s|%s' % (authkey, current_time)
    return authkey_time


url = 'http://127.0.0.1:8000/api/asset/'
app_id = 'alhdlhfkahdlfkhlajejlkjsaldf'
# 添加一个 authkey 用于认证。

header = {
    'authkey': auth_key_time(app_id)
}

host_data = {
    'status': True,
    "data": {
        'hostname': 'ci.com',
        'disk': {'status': True, 'data': 'xxx'},
        'nic': {'status': True, 'data': 'xxx'},
        'memory': {'status': True, 'data': 'xxx'},
    }
}



# 这里不能直接使用 data=host_data 发送过去， 因为发送字典的话，发送到视图中，只能获取到字典的key， value获取不到
# 所以要使用 json=host_data  进行发送。 就是发送一个json字符串过去。 这样视图中就可以通过 request.body 获取到所有的数据
response = requests.post(url=url, json=host_data, headers=header)
# response = requests.get(url=url, params=host_data)

print(response.text)
