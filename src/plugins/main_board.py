#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "nothing"
# Date: 2019/5/20
import os
import traceback
from .base import BasePlugin
from lib.response import BaseResponse


class MainBoardPlugin(BasePlugin):
    '''主板获取'''
    def linux(self):
        response = BaseResponse()
        try:
            if self.test_mode:
                from conf.settings import BASEDIR
                output = open(os.path.join(BASEDIR, 'files/board.out'), 'r').read()
            else:
                shell_comment = 'sudo dmidecode -t1'
                output = self.exec_shell_cmd(shell_comment)
            response.data = self.parse(output)
        except Exception as e:
            msg = "%s linux mainboard plugin error: %s"
            self.logger.log(msg %(self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg %(self.hostname, traceback.format_exc())
        print('Board data', response.data)
        print('Board error', response.error)
        print('Board message', response.message)
        print('Board error', response.error)
        print()
        return response

    @staticmethod
    def parse(content):
        result = {}
        key_map = {
            'Manufacturer': 'manufacturer',  # 制造商
            'Product Name': 'model',  # 类型
            'Serial Number': 'sn',  # SN号
        }
        for item in content.split('\n'):
            row_data = item.strip().split(":")
            if len(row_data) == 2:
                if row_data[0] in key_map:
                    result[key_map[row_data[0]]] = row_data[1].strip()
        '''
        {
        'manufacturer': 'Parallels Software International Inc.', 
        'model': 'Parallels Virtual Platform', 
        'sn': 'Parallels-1A 1B CB 3B 64 66 4B 13 86 B0 86 FF 7E 2B 20 30'
        }
        '''
        return result