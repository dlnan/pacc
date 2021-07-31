from ..adb import ADB, UIAutomator
from datetime import datetime


class Project:

    def __init__(self, deviceSN):
        self.adbIns = ADB(deviceSN)
        self.uIAIns = UIAutomator(deviceSN)
        self.lastReopenHour = -1

    def reopenAppPerHour(self):
        if self.lastReopenHour == datetime.now().hour:
            return False
        self.lastReopenHour = datetime.now().hour
        self.reopenApp()
        return True

    def tapFreeButton(self):
        if 'MI 4' in self.adbIns.device.Model:
            self.uIAIns.tap((540, 1706))

    def reopenApp(self):
        pass

    def openApp(self, activity):
        self.adbIns.start(activity)

    def freeMemory(self):
        self.adbIns.pressHomeKey()
        self.adbIns.pressHomeKey()
        self.adbIns.pressMenuKey()
        self.tapFreeButton()

    def mainloop(self):
        pass
