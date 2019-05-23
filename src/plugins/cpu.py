#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "nothing"
# Date: 2019/5/22
import os
import traceback
from .base import BasePlugin
from lib.response import BaseResponse


class CpuPlugin(BasePlugin):
    def linux(self):
        response = BaseResponse()
        try:
            if self.test_mode:
                from conf.settings import BASEDIR
                output = open(os.path.join(BASEDIR, 'files', 'cpuinfo.out'), 'r').read()
            else:
                shell_comment = 'cat /proc/cpuinfo'
                output = self.exec_shell_cmd(shell_comment)
            response.data = self.parse(output)
        except Exception as e:
            msg = "%s linux cpu plugin error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        print('Cpu data', response.data)
        print('Cpu error', response.error)
        print('Cpu message', response.message)
        print('Cpu error', response.error)
        print()
        return response

    @staticmethod
    def parse(content):
        """
        解析shell命令返回结果
        :param content: shell 命令结果
        :return:解析后的结果
        """
        response = {'cpu_count': 0, 'cpu_physical_count': 0, 'cpu_model': ''}
        #  cup 个数(虚拟的也算)   cpu_physical_count 物理cpu 真实存在的。    cpu_model cpu的类型

        cpu_physical_set = set()  # 用于过滤出是否使物理cpu 还是虚拟cpu。  两个编号  1 和 0

        '''
        processor	: 3
        vendor_id	: GenuineIntel
        cpu family	: 6
        model		: 62
        model name	: Intel(R) Xeon(R) CPU E5-2620 v2 @ 2.10GHz
        stepping	: 4
        cpu MHz		: 2099.921
        cache size	: 15360 KB
        '''

        content = content.strip()
        for item in content.split('\n\n'):
            for row in item.split('\n'):
                key, value = row.split(":")
                key = key.strip()
                if key == 'processor': #   第几个cpu
                    response['cpu_count'] += 1
                elif key == 'physical id':
                    cpu_physical_set.add(value)  #
                elif key == 'model name':
                    if not response['cpu_model']:  # 型号都一样添加一次
                        response['cpu_model'] = value

        response['cpu_physical_count'] = len(cpu_physical_set)
        # {'cpu_count': 24, 'cpu_physical_count': 2, 'cpu_model': ' Intel(R) Xeon(R) CPU E5-2620 v2 @ 2.10GHz'}
        return response
