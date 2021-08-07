from pacc.multi.thread import Thread
from time import sleep

print(Thread.instances)
ins = Thread('')
print(Thread.instances)
ins.__del__()
print(Thread.instances)
