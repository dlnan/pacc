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
        self.currentFocus = ''

    def viewAds(self):
        pass

    @classmethod
    def updateWealthWithMulti(cls, devicesSN):
        runThreadsWithArgsList(cls.initIns, devicesSN)
        functions = []
        for i in cls.instances:
            functions.append(i.updateWealth)
        runThreadsWithFunctions(functions)

    def enterWealthInterface(self):
        pass

    def updateWealth(self, reopen=True):
        if reopen:
            self.reopenApp()
        try:
            if not self.uIAIns.click(resourceID.red_packet_anim
                                     ) and activity.MiniAppActivity0 in self.adbIns.getCurrentFocus():
                self.randomSwipe(True)
                self.updateWealth(False)
            sleep(9)
            self.uIAIns.getCurrentUIHierarchy()
            print('已进入财富界面')
            if self.uIAIns.click('', '立即领取今日现金'):
                self.uIAIns.xml = ''
                self.updateWealth()
                return
            if self.uIAIns.click('', '明天继续领现金', xml=self.uIAIns.xml):
                self.uIAIns.xml = ''
            if self.uIAIns.click('', '立即签到', xml=self.uIAIns.xml):
                self.uIAIns.xml = ''
            if self.uIAIns.click('', '打开签到提醒', xml=self.uIAIns.xml):
                self.uIAIns.xml = ''
            if self.uIAIns.click('', '看广告再得', xml=self.uIAIns.xml):
                sleep(60)
                self.adbIns.pressBackKey()
                self.uIAIns.xml = ''
            if self.uIAIns.click(bounds=bounds.closeInviteFriendsToMakeMoney, xml=self.uIAIns.xml):
                self.uIAIns.xml = ''
            goldCoins, cashCoupons = self.getWealth()
            if not goldCoins == self.dbr.goldCoins:
                UpdateKSJSB(self.adbIns.device.SN).updateGoldCoins(goldCoins)
            if not cashCoupons == self.dbr.cashCoupons:
                UpdateKSJSB(self.adbIns.device.SN).updateCashCoupons(cashCoupons)
        except FileNotFoundError as e:
            print(e)
            self.updateWealth(False)

    def getWealth(self):
        return float(self.uIAIns.getDict(bounds=bounds.goldCoins, xml=self.uIAIns.xml)['@text']),\
               float(self.uIAIns.getDict(bounds=bounds.cashCoupons, xml=self.uIAIns.xml)['@text'])

    def randomSwipe(self, initRestTime=False):
        if initRestTime and self.restTime > 0:
            self.restTime = 0
        elif self.restTime > 0:
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
                self.uIAIns.xml = ''
            if self.uIAIns.click(resourceID.iv_close_common_dialog, xml=self.uIAIns.xml):
                self.uIAIns.xml = ''
            if self.uIAIns.click(resourceID.positive, xml=self.uIAIns.xml):
                self.uIAIns.xml = ''
        except (FileNotFoundError, xml.parsers.expat.ExpatError) as e:
            print(e)
            self.randomSwipe(True)
            sleep(6)
            self.openApp(False)

    def reopenApp(self):
        self.freeMemory()
        self.openApp()

    def shouldReopen(self):
        if activity.KRT1Activity in self.currentFocus:
            return True
        elif 'com.kuaishou.nebula' not in self.currentFocus:
            return True
        return False

    def pressBackKey(self):
        activities = [
            activity.PhotoDetailActivity,
            activity.MiniAppActivity0,
            activity.TopicDetailActivity,
            activity.UserProfileActivity,
            activity.AdYodaActivity
        ]
        for a in activities:
            if a in self.currentFocus:
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
        if self.reopenAppPerHour():
            self.adbIns.keepOnline()
        try:
            if datetime.now().hour > 8 and self.uIAIns.getDict(resourceID.red_packet_anim):
                if not self.uIAIns.getDict(resourceID.cycle_progress, xml=self.uIAIns.xml):
                    self.freeMemory()
                    self.adbIns.pressPowerKey()
                    self.startDay = (datetime.now()+timedelta(days=1)).day
                    return
            self.currentFocus = self.adbIns.getCurrentFocus()
            self.pressBackKey()
            self.initSleepTime()
            if self.shouldReopen():
                self.reopenApp()
        except (FileNotFoundError, xml.parsers.expat.ExpatError) as e:
            print(e)
            self.randomSwipe(True)
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
                if not datetime.now().day == i.startDay:
                    continue
                elif thread:
                    functions.append(i.watchVideo)
                else:
                    i.watchVideo()
            if thread:
                if functions:
                    runThreadsWithFunctions(functions)
                else:
                    sleep(1200)
            print('现在是', datetime.now(), '，已运行：', datetime.now() - cls.startTime,
                  sep='', end='\n\n')
