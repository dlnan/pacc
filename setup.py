from setuptools import setup, find_packages

setup(
    name='pacc',  # 包名
    version='0.0.11',  # 版本
    packages=find_packages(),  # 目录下所有文件
    description='Python Android Cluster Control 为使用Python对安卓集群控制进行支持',  # 描述信息
    long_description="""该Python模块用于通过USB或Wifi对Android集群进行控制，集成了ADB、数据库、图像识别、中央控制系统、验证码破解、等功能。
    目前最新版的是0.0.10，主要实现了以下功能：
    1. 抖音全自动抢福袋脚本app中央控制系统
    2. 汉字大英雄全自动看广告脚本app中央控制系统
    3. 淘宝/拼多多全自动远程刷单app中央控制系统
    源码可通过如下渠道获取：
    Gitee：https://gitee.com/coco56/pacc
    Github：https://github.com/cocos56/pacc
    """,  # 完整的描述信息
    author='Coco',  # 作者
    author_email='zj175@139.com',  # 作者邮箱
    url='https://github.com/cocos56/pacc',  # 主页
)
