#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "nothing"
# Date: 2019/5/20

from conf import settings
from lib.log import Logger


class BasePlugin(object):
    def __init__(self, hostname='', platform_str='Linux'):
        # self.platform_str = platform_str
        self.logger = Logger()
        self.test_mode = settings.TEST_MODE
        self.mode_list = ["ssh", "agent", "salt"]

        if hasattr(settings, 'MODE'):
            self.mode = settings.MODE
        else:
            self.mode = 'agent'
        self.hostname = hostname

    def ssh(self, cmd):
        import paramiko
        private_key = paramiko.RSAKey.from_private_key_file(settings.SSH_PRIVATE_KEY)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname, port=settings.SSH_PORT, username=settings.SSH_USER, pkey=private_key)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        # stdin 标准输入的命令。 stdin.write() 可以在命令执行之后，再写入一些东西
            # 比如有些命令需要用户确认时，就可以通过这个命令 输入 yes 进行确认 或者 no 不确认
        # stdout 标准输出的命令
        # stderr 有错误事 返回的内容
        result = stdout.read()  # 读出 返回的内容。
        ssh.close()
        return result

    def agent(self, cmd):
        import subprocess
        output = subprocess.getoutput(cmd)
        return output

    def salt(self, cmd):
        import salt.client

        local = salt.client.LocalClient()
        result = local.cmd(self.hostname, 'cmd.run', [cmd])
        return result[self.hostname]

    def exec_shell_cmd(self, cmd):
        '''
        判断当前的模式， 再根据cmd 指令，向服务器执行命令，得到结果
        :param cmd:  要执行的命令
        :return:  返回 不同指令执行后得到的结果。
        '''
        if self.mode not in self.mode_list:
            raise Exception("settings.mode must be one of ['agent', 'salt', 'ssh']")
        # if hasattr(self, self.mode.lower()):
        #     output = getattr(self,  self.mode.lower())(cmd)
        #     return output
        # else:
        #     raise NameError('没有这个模式')
        output = getattr(self,  self.mode.lower())(cmd)
        return output

    def platform(self):
        pass

    def execute(self):
        return self.linux()

    def linux(self):
        raise Exception('You mast implement linux method')

    def windows(self):
        raise Exception('暂时还不支持window')


