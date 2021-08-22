from pacc.config import Config
from pacc.project import DYJSB

Config.setDebug(True)
DYJSB('003001002').enterWealthInterface()
