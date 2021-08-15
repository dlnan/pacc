from ..project import KSJSB
from .device import Device


class XM4(Device):
    sNs = ['301', '302', '303', '304']

    def __init__(self):
        super(XM4, self).__init__()

    @classmethod
    def watchVideo(cls):
        # KSJSB.updateWealthWithMulti([
        #     '301',
        #     '302',
        #     '303',
        #     '304'
        # ])
        pass
