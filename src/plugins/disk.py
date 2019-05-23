#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "nothing"
# Date: 2019/5/20
import os
import re
import traceback
from .base import BasePlugin
from lib.response import BaseResponse


class DiskPlugin(BasePlugin):
    def linux(self):
        response = BaseResponse()  # 生成一个 响应实例对象
        try:
            if self.test_mode:  # 判断如果是测试模式
                from conf.settings import BASEDIR
                output = open(os.path.join(BASEDIR, 'files/disk.out'), 'r').read()
            else:
                shell_commend = 'sudo MegaCli  -PDList -aALL'  # 此方法需要安装一个工具，用于磁盘阵列情况下也可以使用
                output = self.exec_shell_cmd(shell_commend)
            response.data = self.pasre(output)  # 这是使用 BaseResponse 一个实例对象。比较容易对数据进行操作。
        except Exception as e:
            msg = "%s linux disk plugin error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        print('disk data', response.data)
        print('disk error', response.error)
        print('disk message', response.message)
        print('disk error', response.error)
        print()
        return response
    '''
    Enclosure Device ID: 32
    Slot Number: 0
    Drive's postion: DiskGroup: 0, Span: 0, Arm: 0
    Enclosure position: 0
    Device Id: 0
    WWN: 5000C5007272C288
    Sequence Number: 2
    Media Error Count: 0
    Other Error Count: 0
    .......
    '''
    def pasre(self, content):
        '''
        解析 shell 命令返回的结果， 取得有用的信息。
        :param content:  shell 命令的结果
        :return:  解析后的结果
        '''
        response = {}
        result = []
        for row_line in content.split('\n\n\n\n'):  # 第一次分割， 因为有很多服务器的， 每个服务器进行区分
            result.append(row_line)
        for item in result:  # 取出每一台服务器的数据
            temp_dict = {}
            for row in item.split('\n'):  # 遍历每一行的数据
                if not row:
                    continue
                if len(row.split(':')) != 2:
                    continue
                key, value = row.split(':')   # PD Type: SATA
                name = self.mega_patter_match(key)
                if name:
                    if key == 'Raw Size':
                        raw_size = re.search('(\d+\.\d+)', value.strip())   # Raw Size: 476.939 GB [0x3b9e12b0 Sectors]
                        if raw_size:
                            temp_dict[name] = raw_size.group()  # re 的search，匹配到的内容需要 group() 才能拿到
                        else:
                            raw_size = 0
                    else:
                        temp_dict[name] = value.strip()
            if temp_dict:
                response[temp_dict['slot']] = temp_dict  # 使用槽位作为键，每个槽位一个磁盘
        ''' {
            '0': {'slot': '0', 'pd_type': 'SAS', 'capacity': '279.396', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'},
            '1': {'slot': '1', 'pd_type': 'SAS', 'capacity': '279.396', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5AH'}, 
            '2': {'slot': '2', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1SZNSAFA01085L     Samsung SSD 850 PRO 512GB               EXM01B6Q'}, 
            '3': {'slot': '3', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1AXNSAF912433K     Samsung SSD 840 PRO Series              DXM06B0Q'}, 
            '4': {'slot': '4', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1AXNSAF303909M     Samsung SSD 840 PRO Series              DXM05B0Q'}, 
            '5': {'slot': '5', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1AXNSAFB00549A     Samsung SSD 840 PRO Series              DXM06B0Q'}
            }
        '''
        return response

    @staticmethod
    def mega_patter_match(needle):
        '''
        从获得的所有的数据中，过滤出需要的内容
        :param needle:
        :return:
        '''
        # 插槽  容量  类型  接口类型
        grep_partten = {'Slot': 'slot', 'Raw Size': 'capacity', 'Inquiry': 'model', 'PD Type': 'pd_type'}
        for key, value in grep_partten.items():
            if needle.startswith(key):  # 如果想要的信息，是以规定的字符串开头，则拿到这个数据， 否则返回False
                return value
        return False
