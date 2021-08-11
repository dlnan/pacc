from ...tools import sleep, findAllWithRe
from ..project import Project


class Activity:
    LauncherUI = 'com.tencent.mm/com.tencent.mm.ui.LauncherUI'  # 微信程序
    Launcher = 'com.miui.home/com.miui.home.launcher.Launcher'  # 桌面


class ResourceID:
    nk = 'com.tencent.mm:id/nk'  # 主界面未读总消息数【微信(9)】
    iot = 'com.tencent.mm:id/iot'  # 主界面未读项（多个对话框）
    auk = 'com.tencent.mm:id/auk'  # 聊天界面消息项（多条消息）


class MM(Project):
    def __init__(self, deviceSN):
        super(MM, self).__init__(deviceSN, False)

    def enterLatestMsgInterface(self):
        self.reopenApp()
        if self.uIAIns.click(ResourceID.iot):
            return True

    def getLatestMsg(self):
        if not self.enterLatestMsgInterface():
            return
        res = self.uIAIns.getDicts(ResourceID.auk)
        if res:
            return res[-1]['@text']

    def getLatestURL(self):
        res = self.getLatestMsg()
        if res:
            res = findAllWithRe(res, r'https?://\S+')
        print(res)
        res = res[0] if len(res) == 1 else None
        print(res)
        self.exitApp()
        return res

    def sendURL(self):
        url = self.getLatestURL()
        pass

    def exitApp(self):
        self.openApp(1)
        while Activity.Launcher not in self.adbIns.getCurrentFocus():
            self.adbIns.pressBackKey()

    def reopenApp(self):
        self.exitApp()
        super(MM, self).reopenApp()

    def openApp(self, interval=6):
        super(MM, self).openApp(Activity.LauncherUI)
        sleep(interval)
