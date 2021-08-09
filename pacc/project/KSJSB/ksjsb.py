from datetime import datetime, timedelta
from time import time
from xml.parsers.expat import ExpatError
from ...tools import sleep
from ...mysql import RetrieveKSJSB, UpdateKSJSB
from pacc.multi import runThreadsWithArgsList, runThreadsWithFunctions, threadLock
from ..project import Project
from . import resourceID, activity, bounds


class KSJSB(Project):
    def __init__(self, deviceSN):
        super(KSJSB, self).__init__(deviceSN)
        self.startDay = datetime.now().day
        self.dbr = RetrieveKSJSB(deviceSN)
        self.currentFocus = ''

    def watchLive(self):
        self.enterWealthInterface()
        self.randomSwipe(True)
        while True:
            try:
                while self.uIAIns.getCP(text='观看精彩直播得110金币') == (0, 0):
                    self.randomSwipe(True)
                if not self.uIAIns.getDict(text='看直播领1100金币'):
                    self.watchLive()
                    return
                if self.uIAIns.click(text='观看精彩直播得110金币'):
                    sleep(20)
                    if activity.PhotoDetailActivity not in self.adbIns.getCurrentFocus():
                        self.watchLive()
                        return
                    sleep(60)
                    self.exitLive()
                else:
                    break
            except FileNotFoundError as e:
                print(e)
                self.watchLive()

    def exitLive(self, currentFocus=''):
        if not currentFocus:
            currentFocus = self.adbIns.getCurrentFocus()
        if activity.PhotoDetailActivity in currentFocus:
            #  关闭5元优惠券
            if self.uIAIns.getDict(resourceID.live_follow_guide_card_button):
                self.adbIns.pressBackKey()
                self.uIAIns.xml = ''
            if self.uIAIns.click(resourceID.dialog_close, xml=self.uIAIns.xml):  # 关闭新人限时购物红包（10.99元）
                self.uIAIns.xml = ''
            self.adbIns.pressBackKey()
            if self.uIAIns.click(resourceID.live_exit_button, xml=self.uIAIns.xml):
                self.uIAIns.xml = ''
            self.uIAIns.click(resourceID.exit_btn, xml=self.uIAIns.xml)
        if activity.PhotoDetailActivity in self.adbIns.getCurrentFocus():
            self.exitLive()

    def viewAds(self):
        self.enterWealthInterface()
        self.randomSwipe(True)
        while True:
            try:
                if activity.KwaiYodaWebViewActivity not in self.adbIns.getCurrentFocus():
                    self.viewAds()
                    return
                elif self.uIAIns.click(text='观看广告单日最高可得5000金币') or self.uIAIns.click(
                        text='每次100金币，每天1000金币', xml=self.uIAIns.xml):
                    sleep(50)
                    self.adbIns.pressBackKey()
                else:
                    break
            except FileNotFoundError as e:
                print(e)
                self.viewAds()

    def enterWealthInterface(self, reopen=True):
        if reopen:
            self.reopenApp()
        try:
            if not self.uIAIns.click(resourceID.red_packet_anim, xml=self.uIAIns.xml
                                     ) and activity.MiniAppActivity0 in self.adbIns.getCurrentFocus():
                self.randomSwipe(True)
                self.enterWealthInterface(False)
                return
            sleep(18)
            self.uIAIns.getCurrentUIHierarchy()
            print('已进入财富界面')
            if self.uIAIns.click('', '立即领取今日现金'):
                self.uIAIns.xml = ''
                self.enterWealthInterface()
                return
            if self.uIAIns.click('', '立即签到', xml=self.uIAIns.xml):
                self.uIAIns.xml = ''
            if self.uIAIns.click('', '打开签到提醒', xml=self.uIAIns.xml):  # 需要授权
                self.uIAIns.xml = ''
            elif self.uIAIns.click('', '看广告再得', xml=self.uIAIns.xml):
                sleep(60)
                self.adbIns.pressBackKey()
                self.uIAIns.xml = ''
            if self.uIAIns.click(bounds=bounds.closeInviteFriendsToMakeMoney, xml=self.uIAIns.xml):
                self.uIAIns.xml = ''
            elif self.uIAIns.click(bounds=bounds.closeCongratulations, xml=self.uIAIns.xml):
                self.uIAIns.xml = ''
        except FileNotFoundError as e:
            print(e)
            self.enterWealthInterface(False)

    @classmethod
    def updateWealthWithMulti(cls, devicesSN):
        runThreadsWithArgsList(cls.initIns, devicesSN)
        functions = []
        for i in cls.instances:
            functions.append(i.updateWealth)
        runThreadsWithFunctions(functions)

    def updateWealth(self, reopen=True):
        self.enterWealthInterface(reopen)
        try:
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

    def openApp(self, reopen=True):
        if reopen:
            super(KSJSB, self).openApp(activity.HomeActivity)
            sleep(18)
        try:
            if self.uIAIns.click(resourceID.close):
                self.uIAIns.xml = ''
            if self.uIAIns.click(resourceID.iv_close_common_dialog, xml=self.uIAIns.xml):
                self.uIAIns.xml = ''
            if self.uIAIns.click(resourceID.positive, xml=self.uIAIns.xml):
                self.uIAIns.xml = ''
            if self.uIAIns.click(resourceID.tv_upgrade_now, xml=self.uIAIns.xml):
                self.uIAIns.xml = ''
                self.adbIns.pressBackKey()
        except (FileNotFoundError, ExpatError) as e:
            print(e)
            self.randomSwipe(True)
            sleep(6)
            self.openApp(False)

    def shouldReopen(self):
        if activity.KRT1Activity in self.currentFocus:
            return True
        elif activity.MiniAppActivity0 in self.currentFocus:
            return True
        elif 'com.kuaishou.nebula' not in self.currentFocus:
            return True
        return False

    def pressBackKey(self):
        activities = [
            activity.TopicDetailActivity,
            activity.UserProfileActivity,
            activity.AdYodaActivity
        ]
        for a in activities:
            if a in self.currentFocus:
                self.adbIns.pressBackKey()
                break
        if self.uIAIns.getDict(resourceID.tab_text, xml=self.uIAIns.xml):
            self.adbIns.pressBackKey()
            self.uIAIns.xml = ''
        if self.uIAIns.getDict(resourceID.choose_tv, xml=self.uIAIns.xml):
            self.adbIns.pressBackKey()
            self.randomSwipe(True)
            self.uIAIns.xml = ''

    def initSleepTime(self):
        print('restTime=%s' % self.restTime)
        if self.restTime <= 0:
            return
        elif self.uIAIns.getDict(resourceID.live_simple_play_swipe_text, xml=self.uIAIns.xml):
            pass
        elif self.uIAIns.getDict(resourceID.open_long_atlas, xml=self.uIAIns.xml):
            pass
        else:
            return
        self.restTime = 0

    def watchVideo(self):
        if self.reopenAppPerHour():
            self.adbIns.keepOnline()
        try:
            if datetime.now().hour > 5 and self.uIAIns.getDict(resourceID.red_packet_anim):
                if not self.uIAIns.getDict(resourceID.cycle_progress, xml=self.uIAIns.xml):
                    self.freeMemory()
                    self.adbIns.pressPowerKey()
                    self.startDay = (datetime.now()+timedelta(days=1)).day
                    return
            self.uIAIns.click(resourceID.button2)
            self.currentFocus = self.adbIns.getCurrentFocus()
            self.pressBackKey()
            self.exitLive(self.currentFocus)
            self.initSleepTime()
            if self.shouldReopen():
                self.reopenApp()
        except (FileNotFoundError, ExpatError) as e:
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
