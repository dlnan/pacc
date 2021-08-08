from ..project import KSJSB
from .device import Device


class XM4(Device):
    sNs = ['301', '302', '303', '304']

    def __init__(self):
        super(XM4, self).__init__()

    @classmethod
    def viewAds(cls):
        for sN in cls.sNs:
            KSJSB(sN).viewAds()

    @classmethod
    def watchLive(cls):
        for sN in cls.sNs:
            KSJSB(sN).watchLive()

    @classmethod
    def updateWealth(cls):
        for sN in cls.sNs:
            KSJSB(sN).updateWealth()

    @classmethod
    def watchVideo(cls):
        # KSJSB.updateWealthWithMulti([
        #     '301',
        #     '302',
        #     '303',
        #     '304'
        # ])
        pass
