from setuptools import setup, find_packages

setup(
    name='pacc',  # 包名
    version='0.0.258',  # 版本
    packages=find_packages(),  # 目录下所有文件
    description="""Python Android Cluster Control 为在Windows上使用Python通过USB（通用串行总线）或
                    WLAN（基于IPv4的无线局域网）对Android手机集群的控制提供支持""",  # 描述信息
    long_description="""该Python模块用于通过USB或WiFi对Android集群进行控制，
    集成了ADB、UIAutomator、数据库、中央控制系统、计算机视觉（图像识别）、验证码破解、人工智能（自然语言处理）等功能。\n
    目前最新版已集成的功能如下：\n
    1. ADB（安卓调试桥）及UIAutomator（用户界面自动化器）\n
    2. MySQL数据库\n
    已实现的中央监控系统如下：\n
    1. 淘宝/拼多多全自动远程刷单app中央控制系统\n
    2. 汉字大英雄全自动看广告脚本app中央控制系统\n
    待实现的中央监控系统如下：\n
    1. 欢友全自动聊天、评论、接打视频脚本app中央监控系统\n
    已实现的中央控制脚本如下：\n
    1. 快手极速版全自动刷金币（刷视频、刷广告、刷直播）中央控制脚本\n
    2. 抖音极速版全自动刷金币中央控制脚本\n
    待实现的中央控制脚本如下：\n
    1. 点淘全自动刷金币中央控制脚本\n
    2. 抖音全自动抢福袋脚本app中央控制脚本\n
    3. 淘礼金全自动抢单（淘宝0元购）中央控制脚本\n
    4. 他趣全自动拉黑女粉、聊天、接视频中央控制脚本\n
    源码可通过如下渠道获取：\n
    Gitee：https://gitee.com/coco56/pacc\n
    Github：https://github.com/cocos56/pacc\n
    """,  # 完整的描述信息
    author='Coco',  # 作者
    author_email='zj175@139.com',  # 作者邮箱
    url='https://github.com/cocos56/pacc',  # 主页
)
