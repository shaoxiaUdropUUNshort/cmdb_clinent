#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json as default_json
from json.encoder import JSONEncoder
from .response import BaseResponse


class MyJsonEncoder(JSONEncoder):
    def default(self, o):  # 这个 o 就是每一个 BaseResponse 的实例对象。
        if isinstance(o, BaseResponse):
            # print(o.__dict__)
            return o.__dict__  # 取出对象的内置字典中的数据
        return JSONEncoder.default(self, o)  # 然后进行序列化。


class Json(object):
    @staticmethod
    def dumps(response, ensure_ascii=True):
        # response是一个字典： 其中的  cpu disk board memory nic 都是类的对象。还有一些普通的字典类型的值。就正常序列化
        return default_json.dumps(response, ensure_ascii=ensure_ascii, cls=MyJsonEncoder)
        # 告诉json.dumps 使用我自己定义的的cls 类， 进行序列化。
















