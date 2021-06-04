from os import popen, system
from ..tools import findAllWithRe, sleep
from random import randint


class ADB:

    def __init__(self, device):
        """
        :param device: Device IP or Device ID
        """
        self.device = device
        self.cmd = 'adb -s %s ' % device

    def connect(self):
        system(self.cmd + 'connect')


    def tap(self, x, y):
        system(self.cmd + 'shell input tap %d %d' % (x, y))

    def start(self, Activity, wait=True):
        cmd = 'shell am start '
        if wait:
            cmd += '-W '
        system(self.cmd + cmd + Activity)

    def swipe(self, x1, y1, x2, y2, duration=-1):
        """
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :param duration: the default duration is a random integer from 300 to 500
        :return:
        """
        if duration == -1:
            duration = randint(300, 500)
        system(self.cmd + 'shell input swipe %d %d %d %d %d' % (x1, y1, x2, y2, duration))

    def longPress(self, x, y, duration=-1):
        """
        :param x:
        :param y:
        :param duration: the default duration is a random integer from 1000 to 1500
        :return:
        """
        if duration == -1:
            duration = randint(1000, 1500)
        self.swipe(x, y, x, y, duration)

    def reboot(self, interval=60):
        system(self.cmd + 'reboot')
        print('已向设备%s下达重启指令' % self.device)
        sleep(interval)

    def getIPv4Address(self):
        rd = popen(self.cmd + 'shell ifconfig wlan0').read()
        IPv4Address = findAllWithRe(rd, r'inet addr:(\d+.\d+.\d+.\d+)  Bcast:.+')
        if len(IPv4Address) == 1:
            IPv4Address = IPv4Address[0]
        # print(IPv4Address)
        return IPv4Address

    def getIPv6Address(self):
        rd = popen(self.cmd + 'shell ifconfig wlan0').read()
        # print(rd)
        IPv6Address = findAllWithRe(rd, r'inet6 addr: (.+:.+:.+)/64 Scope: Global')
        if len(IPv6Address) <= 2:
            IPv6Address = IPv6Address[0]
            print('设备%s的公网IPv6地址为：%s' % (self.device, IPv6Address))
        else:
            print('%s的公网IPv6地址数大于2，正在尝试重新获取')
            self.reboot()
            self.getIPv6Address()
