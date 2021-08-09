from datetime import datetime
from random import randint
from time import time
from ..adb import ADB, UIAutomator


class ResourceID:
    clearAnimView = 'com.android.systemui:id/clearAnimView'  # 内存清理图标


class Project:
    instances = []
    startTime = datetime.now()

    def __init__(self, deviceSN):
        self.adbIns = ADB(deviceSN)
        self.uIAIns = UIAutomator(deviceSN)
        self.lastReopenHour = -1
        self.restTime = 0
        self.lastTime = time()

    def randomSwipe(self, initRestTime=False):
        if initRestTime and self.restTime > 0:
            self.restTime = 0
        elif self.restTime > 0:
            return
        x1 = randint(360, 390)
        y1 = randint(1160, 1190)
        x2 = randint(360, 390)
        y2 = randint(260, 290)
        self.adbIns.swipe(x1, y1, x2, y2)
        self.restTime += randint(3, 15)

    def reopenAppPerHour(self):
        if self.lastReopenHour == datetime.now().hour:
            return False
        self.lastReopenHour = datetime.now().hour
        self.reopenApp()
        return True

    def tapFreeButton(self):
        if 'MI 4' in self.adbIns.device.Model:
            self.uIAIns.click(ResourceID.clearAnimView)

    def reopenApp(self):
        self.freeMemory()
        self.openApp()

    def openApp(self, activity):
        self.adbIns.start(activity)

    def freeMemory(self):
        self.adbIns.pressHomeKey()
        self.adbIns.pressHomeKey()
        self.adbIns.pressMenuKey()
        try:
            self.tapFreeButton()
        except FileNotFoundError as e:
            print(e)
            self.freeMemory()

    def mainloop(self):
        pass
