import xml
from random import randint
from datetime import datetime, timedelta
from time import time
from ...tools import sleep
from ...mysql import RetrieveKSJSB, UpdateKSJSB
from ...Multi import runThreadsWithArgsList, runThreadsWithFunctions, threadLock
from ..project import Project
from . import resourceID, activity, bounds


class KSJSB(Project):
    instances = []
    startTime = datetime.now()

    def __init__(self, deviceSN):
        super(KSJSB, self).__init__(deviceSN)
        self.restTime = 0
        self.startDay = datetime.now().day
        self.lastTime = time()
        self.dbr = RetrieveKSJSB(deviceSN)

    @classmethod
    def updateWealthWithMulti(cls, devicesSN):
        runThreadsWithArgsList(cls.initIns, devicesSN)
        functions = []
        for i in cls.instances:
            functions.append(i.updateWealth)
        runThreadsWithFunctions(functions)

    def updateWealth(self, reopen=True):
        if reopen:
            self.reopenApp()
        try:
            if not self.uIAIns.click(resourceID.red_packet_anim
                                     ) and activity.MiniAppActivity0 in self.adbIns.getCurrentFocus():
                self.randomSwipe(True)
                self.updateWealth(False)
            sleep(9)
            while self.uIAIns.click(bounds=bounds.attendance):
                pass
            goldCoins, cashCoupons = self.getWealth()
            if not goldCoins == self.dbr.goldCoins:
                UpdateKSJSB(self.adbIns.device.SN).updateGoldCoins(goldCoins)
            if not cashCoupons == self.dbr.cashCoupons:
                UpdateKSJSB(self.adbIns.device.SN).updateCashCoupons(cashCoupons)
        except FileNotFoundError as e:
            print(e)
            self.updateWealth(False)

    def getWealth(self):
        gCDic = self.uIAIns.getDict(bounds=bounds.goldCoins)
        cCDic = self.uIAIns.getDict(bounds=bounds.cashCoupons, xml=self.uIAIns.xml)
        if not cCDic:
            cCDic = self.uIAIns.getDict(bounds=bounds.cashCoupons2, xml=self.uIAIns.xml)
        return gCDic['@text'], cCDic['@text']

    def randomSwipe(self, initRestTime=False):
        if initRestTime and self.restTime > 0:
            self.restTime = 0
        if self.restTime > 0:
            return
        x1 = randint(520, 550)
        y1 = randint(1530, 1560)
        x2 = randint(520, 550)
        y2 = randint(360, 390)
        self.adbIns.swipe(x1, y1, x2, y2)
        self.restTime += randint(3, 15)

    def openApp(self, reopen=True):
        if reopen:
            super(KSJSB, self).openApp(activity.HomeActivity)
            sleep(12)
        try:
            if self.uIAIns.click(resourceID.close):
                self.uIAIns.click(resourceID.iv_close_common_dialog)
            else:
                self.uIAIns.click(resourceID.iv_close_common_dialog, xml=self.uIAIns.xml)
        except (FileNotFoundError, xml.parsers.expat.ExpatError) as e:
            print(e)
            self.openApp(False)

    def reopenApp(self):
        self.freeMemory()
        self.openApp()

    def shouldReopen(self):
        pass

    def pressBackKey(self):
        currentFocus = self.adbIns.getCurrentFocus()
        activities = [
            activity.PhotoDetailActivity,
            activity.MiniAppActivity0,
            activity.TopicDetailActivity,
            activity.UserProfileActivity,
            activity.AdYodaActivity
        ]
        for a in activities:
            if a in currentFocus:
                self.adbIns.pressBackKey()
                break
        resourcesID = [
            resourceID.tab_text,
            resourceID.comment_header_close,
            resourceID.tv_upgrade_now
        ]
        for rID in resourcesID:
            if self.uIAIns.getDict(rID, xml=self.uIAIns.xml):
                self.adbIns.pressBackKey()
                break
        self.uIAIns.click(resourceID.live_exit_button, xml=self.uIAIns.xml)
        self.uIAIns.click(resourceID.exit_btn, xml=self.uIAIns.xml)
        self.uIAIns.click(resourceID.button2, xml=self.uIAIns.xml)

    def initSleepTime(self):
        print('restTime=%s' % self.restTime)
        if self.restTime <= 0:
            return
        elif self.uIAIns.getDict(resourceID.live_simple_play_swipe_text, xml=self.uIAIns.xml):
            pass
        elif self.uIAIns.getDict(resourceID.open_long_atlas, xml=self.uIAIns.xml):
            pass
        elif self.uIAIns.getDict(resourceID.choose_tv, xml=self.uIAIns.xml):
            pass
        else:
            return
        self.restTime = 0

    def watchVideo(self):
        self.reopenAppPerHour()
        try:
            if not datetime.now().day == self.startDay:
                sleep(600)
                return
            if datetime.now().hour > 8 and self.uIAIns.getDict(resourceID.red_packet_anim):
                if not self.uIAIns.getDict(resourceID.cycle_progress, xml=self.uIAIns.xml):
                    self.freeMemory()
                    sleep(600)
                    self.startTime = (datetime.now()+timedelta(days=1)).day
                    return
            self.pressBackKey()
            self.initSleepTime()
        except (FileNotFoundError, xml.parsers.expat.ExpatError) as e:
            print(e)
        self.restTime = self.restTime + self.lastTime - time()
        self.lastTime = time()
        self.randomSwipe()
        self.uIAIns.xml = ''

    @classmethod
    def initIns(cls, deviceSN):
        ins = cls(deviceSN)
        threadLock.acquire()
        cls.instances.append(ins)
        threadLock.release()

    @classmethod
    def mainloop(cls, devicesSN, thread=True):
        runThreadsWithArgsList(cls.initIns, devicesSN)
        while True:
            functions = []
            for i in cls.instances:
                if thread:
                    functions.append(i.watchVideo)
                else:
                    i.watchVideo()
            if thread:
                runThreadsWithFunctions(functions)
            print('现在是', datetime.now(), '，已运行：', datetime.now() - cls.startTime,
                  sep='', end='\n\n')
