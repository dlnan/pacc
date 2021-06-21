from setuptools import setup, find_packages

setup(
    name='pacc',  # 包名
    version='0.0.5',  # 版本
    packages=find_packages(),  # 目录下所有文件
    description='Python Android Cluster Control 为使用Python对安卓集群控制进行支持',  # 描述信息
    long_description='安卓集群控制系统模块，包含对ADB、数据库、图像识别、验证码破解等功能的封装',  # 完整的描述信息
    author='Coco',  # 作者
    author_email='zj175@139.com',  # 作者邮箱
    url='https://github.com/cocos56/pacc',  # 主页
)
