import threading
import time

taskRunFlag = False
taskStartFlag = False

class terminalThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            global taskRunFlag,taskStartFlag
            cmd = input()
            if not taskRunFlag:
                taskStartFlag = True

ternimalthread = terminalThread()
ternimalthread.start()


while True:
    while not taskStartFlag:
        time.sleep(0.1)
    taskRunFlag = True
    taskStartFlag = False
    print('taskStart')
    time.sleep(1)
    print('taskStop')
    taskRunFlag = False
    print(taskRunFlag,taskStartFlag)