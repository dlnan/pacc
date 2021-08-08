from ..project import Project


class QQA:
    SplashActivity = 'com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity'  # QQ程序


class MMA:
    LauncherUI = 'com.tencent.mm/com.tencent.mm.ui.LauncherUI'  # 微信程序


class TBA:
    TBMainActivity = 'com.taobao.taobao/com.taobao.tao.TBMainActivity'  # 淘宝程序


class QQRID:
    unchecked_msg_num = 'com.tencent.qqlite:id/unchecked_msg_num'  # 消息按钮
    unreadmsg = 'com.tencent.qqlite:id/unreadmsg'  # 未读消息数（多个）


class TLJ(Project):
    def __init__(self, deviceSN):
        super(TLJ, self).__init__(deviceSN)
        self.uIAIns.getCurrentUIHierarchy()


