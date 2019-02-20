import cv2
import socket
import time
import os
import netifaces as ni
from subprocess import call
import threading

cap = cv2.VideoCapture(0)

taskRunFlag = False
taskStartFlag = False
cmd = ''

class terminalThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            global taskRunFlag,taskStartFlag,cmd
            cmd = input().strip('\n')
            if not taskRunFlag:
                taskStartFlag = True
            if cmd == 'end':
                break

ternimalthread = terminalThread()
ternimalthread.start()

while True:
    while not taskStartFlag:
        pass
    if cmd == 'end':
        break
    taskRunFlag = True
    taskStartFlag = False
    for i in range(5):  #flush the buffer
        cap.read()
    ret,frame = cap.read()
    fpic = open('test.jpg','w')
    cv2.imwrite('test.jpg',frame)
    fpic.close()

    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    packetSize = 8192
    try:
        host = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    except:
        host = socket.gethostname()
    port = 4445
    addr = ('192.168.43.1',port)

    f = open("test.jpg",'rb')
    audiof = open("audio.wav",'wb')

    old_file_position = f.tell()
    f.seek(0, os.SEEK_END)
    fsize = f.tell()
    f.seek(old_file_position, os.SEEK_SET)

    fsizedata = str(fsize).encode()
    #print(fsizedata)

    data = f.read(packetSize)
    while data:
        if(s.sendto(data,addr)):
            data = f.read(packetSize)
        
    s.close()
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.sendto(b"end",addr)
    s.close()
    f.close()

    print("transmit conplete")

    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,port))

    while True:
        data = s.recv(packetSize)
        if data == b'end':
            break
        else:
            audiof.write(data)
    audiof.close()
    print("receive complete")

    s.close() 


    call(["aplay",audiof.name])
    taskRunFlag = False

cap.release()