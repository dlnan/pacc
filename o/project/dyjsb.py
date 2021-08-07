from time import time
from datetime import datetime
from ..tools import sleep
from ..multi import runThreadsWithArgsList, threadLock
from .project import Project


class Activity:
    SplashActivity = 'com.ss.android.ugc.aweme.lite/com.ss.android.ugc.aweme.splash.SplashActivity'  # 抖音程序入口


class DYJSB(Project):
    def __init__(self, deviceSN):
        super(DYJSB, self).__init__(deviceSN)

    def openApp(self):
        super(DYJSB, self).openApp(Activity.SplashActivity)
        sleep(12)

    def watchVideo(self):
        if self.reopenAppPerHour():
            self.adbIns.keepOnline()
        try:
            self.uIAIns.getCurrentUIHierarchy()
        except FileNotFoundError as e:
            print(e)
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
