#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "nothing"
# Date: 2019/5/20

from conf import settings
from importlib import import_module
from src.plugins.basic import BasicPlugin


# 这个代码写在 __init__.py 中。 会在其他模块导入 这个包的时候 自动的加载 __init__.py 中的数据。
# 所以 from src import plugins 时，不需要再去导入 __init__ 就可以拿到  get_server_info 这个方法

# plugins.get_server_info()

def get_server_info(hostname=None):
    '''
    获取服务器信息, 并且将所有的数据进行打包。
    :param hostname: # hostname 为空时，表示要通过agent方式获取。所以不需要主机名。
    :return:
    '''
    response = BasicPlugin(hostname).execute()
    # os_platform_str = response.data['os_platform']  # Linux  or  window  or mac

    if not response.status:  # 如果中途发生了错误，使status值改为false的话。 在这里就返回，不再执行
        return response
    '''
    PLUGINS_DICT = {
      k       v
    'cpu': 'src.plugins.cpu.CpuPlugin',
    'disk': 'src.plugins.disk.DiskPlugin',
    'main_board': 'src.plugins.main_board.MainBoardPlugin',
    'memory': 'src.plugins.memory.MemoryPlugin',
    'nic': 'src.plugins.nic.NicPlugin',
    }
    '''
    # 循环导入配置文件中的需要获取的硬件信息。 并执行每个类的 execute
    for k, v in settings.PLUGINS_DICT.items():
        # src.plugins.cpu   CpuPlugin
        model_path, class_name = v.rsplit(".", maxsplit=1)
        cls = getattr(import_module(model_path), class_name)
        # 利用反射去找到 指定路径下的包， 包中的 类。
        response.data[k] = cls(hostname).execute()
        # 得到想要的类实例化并执行  execute()。 结果保存到字典中。  键就是 k
    return response


'''将打包的工作写入 __init__ 文件。 其他地方只要导入 plugins。就会默认导入 __init__文件
这样， 使用时 只需要  plugins.get_server_info()  就可以。 这就是一个插件。更加符合一个插件的样子

打包的结构：

    {'xx':'xx', cpu的BasicPlugin对象， disk的BasicPlugin对象， nic的BasicPlugin对象}
    这些数据，交给 process 函数的， 自定制Json 进行，序列化。 并发送给API
'''




