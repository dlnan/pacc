from pacc.project import KSJSB
from pacc.config import Config


Config.setDebug(True)
# KSJSB('003001001').signIn()
KSJSB('003001001').updateWealth()
KSJSB('003001002').updateWealth()
KSJSB('003001003').updateWealth()
KSJSB('003001004').updateWealth()
