import threading
from ...tools import sleep

threadLock = threading.Lock()


def runThreadsWithFunctions(functions):
	threads = []
	for function in functions:
		t = runThread(function)
		threads.append(t)
	for t in threads:
		t.join()


def runThreadsWithArgsList(function, argsList):
	threads = []
	for args in argsList:
		t = runThread(function, (args,))
		threads.append(t)
	for t in threads:
		t.join()


def runThread(function, args=(), delay=1):
	sleep(delay)
	if args:
		t = threading.Thread(target=function, args=args)
	else:
		t = threading.Thread(target=function)
	t.start()
	return t
