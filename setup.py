from setuptools import setup, find_packages

setup(
    name='pacc',  # 包名
    version='0.0.86',  # 版本
    packages=find_packages(),  # 目录下所有文件
    description='Python Android Cluster Control 为使用Python对安卓集群控制进行支持',  # 描述信息
    long_description="""该Python模块用于通过USB或Wifi对Android集群进行控制，集成了ADB、UIAutomator、数据库、中央控制系统、图像识别、验证码破解、人工智能、自然语言处理等功能。
    目前最新版已集成的功能如下：
    1. ADB（安卓调试桥）
    2. MySQL数据库
    已实现的中央监控系统如下：
    1. 淘宝/拼多多全自动远程刷单app中央控制系统
    2. 汉字大英雄全自动看广告脚本app中央控制系统
    3. 抖音全自动抢福袋脚本app中央控制系统
    已实现的中央控制脚本如下：
    1. 快手极速版全自动刷金币中央控制脚本
    2. 他趣全自动拉黑女粉、聊天、接视频中央控制脚本
    源码可通过如下渠道获取：
    Gitee：https://gitee.com/coco56/pacc
    Github：https://github.com/cocos56/pacc
    """,  # 完整的描述信息
    author='Coco',  # 作者
    author_email='zj175@139.com',  # 作者邮箱
    url='https://github.com/cocos56/pacc',  # 主页
)
