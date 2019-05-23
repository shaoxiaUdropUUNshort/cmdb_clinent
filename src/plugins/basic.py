#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "nothing"
# Date: 2019/5/22
import traceback
from .base import BasePlugin
from lib.response import BaseResponse


class BasicPlugin(BasePlugin):
    '''主机的基本信息，是必须要获取的。'''
    def os_platform(self):
        '''
        获取系统平台
        :return:
        '''
        if self.test_mode:
            output = 'Linux'
        else:
            output = self.exec_shell_cmd('uname')
        return output

    def os_version(self):
        '''获取 系统版本'''

        if self.test_mode:
            output = 'CentOS release 6.6 (Final)\nKernel \r on an \m'
        else:
            output = self.exec_shell_cmd('cat /etc/issue')
        result = output.strip().split('\n')[0]
        return result

    def os_hostname(self):
        '''获取主机名'''
        if self.test_mode:
            output = 'c1.com'
        else:
            output = self.exec_shell_cmd('hostname')
        return output.strip()

    def linux(self):
        response = BaseResponse()
        try:
            ret = {
                'os_platform': self.os_platform(),  # 'Linux'
                'hostname': self.os_hostname(),  # CentOS
                'os_version': self.os_version()  # c1.com
            }
            response.data = ret
        except Exception as e:
            msg = "%s BasicPlugin Error:%s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())
        print('Basic data', response.data)
        print('Basic error', response.error)
        print('Basic message', response.message)
        print('Basic error', response.error)
        return response


















