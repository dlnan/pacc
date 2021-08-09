from time import time
from datetime import datetime, timedelta
from xml.parsers.expat import ExpatError
from ..tools import sleep
from ..multi import runThreadsWithArgsList, threadLock
from .project import Project


class Activity:
    SplashActivity = 'com.ss.android.ugc.aweme.lite/com.ss.android.ugc.aweme.splash.SplashActivity'  # 抖音极速版程序入口


class ResourceID:
    e5s = 'com.ss.android.ugc.aweme.lite:id/e5s'  # 我知道了（儿童/青少年模式提醒）
    av0 = 'com.ss.android.ugc.aweme.lite:id/av0'  # 关闭（12个红包 超多现金福利）


class DYJSB(Project):
    def __init__(self, deviceSN):
        super(DYJSB, self).__init__(deviceSN)
        self.startDay = datetime.now().day

    def openApp(self):
        super(DYJSB, self).openApp(Activity.SplashActivity)
        sleep(12)
        try:
            if self.uIAIns.click(ResourceID.e5s):
                sleep(3)
                self.uIAIns.xml = ''
            self.uIAIns.click(ResourceID.av0, xml=self.uIAIns.xml)
        except (FileNotFoundError, ExpatError) as e:
            print(e)

    def watchVideo(self):
        if datetime.now().hour > 22 or datetime.now().hour < 7:
            if datetime.now().hour == 23 and datetime.now().day == self.startDay:
                self.freeMemory()
                self.adbIns.pressPowerKey()
                self.startDay = (datetime.now()+timedelta(days=1)).day
            return
        if self.reopenAppPerHour():
            self.adbIns.keepOnline()
        # if Activity.SplashActivity not in self.adbIns.getCurrentFocus():
        #     self.reopenApp()
        self.restTime = self.restTime + self.lastTime - time()
        self.lastTime = time()
        self.randomSwipe()

    @classmethod
    def initIns(cls, deviceSN):
        ins = cls(deviceSN)
        threadLock.acquire()
        cls.instances.append(ins)
        threadLock.release()

    @classmethod
    def mainloop(cls, devicesSN):
        runThreadsWithArgsList(cls.initIns, devicesSN)
        while True:
            for i in cls.instances:
                i.watchVideo()
            sleep(3)
            print('现在是', datetime.now(), '，已运行：', datetime.now() - cls.startTime,
                  sep='', end='\n\n')
