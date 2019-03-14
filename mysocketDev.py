import cv2
import socket
import time
import os
import netifaces as ni
from subprocess import call
import threading
import numpy as np
from scipy.io import wavfile


#parameters for distortion correction
dim=(640, 480)
k=np.array([[383.6314766818211, 0.0, 333.48039436141994], [0.0, 383.1302804389697, 233.7248359166726], [0.0, 0.0, 1.0]])
d=np.array([[-0.12942834439747042], [0.3726097193339902], [-0.9743000811036107], [0.866862732720388]])
map1, map2 = cv2.fisheye.initUndistortRectifyMap(k, d, np.eye(3), k, dim,cv2.CV_16SC2)

'''
Undistort the input image.
Parameters:
img                 an opencv image
Return value:
undistorted_img     an opencv image
'''
def undistort(img):
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)    
    return undistorted_img


'''
Add blank time to the audio file. This function solves the audio play bug.
Parameters:
filepath         path to the audio file
blankTime        blank time, in seconds
'''
def extendTime(filepath,blankTime=0.5):
    try:
        fs, data = wavfile.read(filepath)
        blankAudioLength = blankTime
        blankAudio = np.zeros(int(blankAudioLength*fs),dtype=np.int16)
        newAudio = np.hstack([blankAudio,data])
        print(data.shape)
        print(newAudio.shape)
        wavfile.write(filepath,fs,newAudio)
        return True
    except:
        return False

#parameters for inter-threading communication
taskRunFlag = False
taskStartFlag = False
cmd = ''

'''
This thread handles the terminal input.
'''
class terminalThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    '''
    If receives a line that is not "end", start a recognition task.
    If receives "end", stop this thread.
    '''
    def run(self):
        while True:
            global taskRunFlag,taskStartFlag,cmd
            cmd = input().strip('\n')
            if not taskRunFlag:
                taskStartFlag = True
            if cmd == 'end':
                break

#create and start the thread.
ternimalthread = terminalThread()
ternimalthread.start()

#play power on audio.
call(["aplay","poweron.wav"])

while True:
    #End the loop if cmd is end.
    while not taskStartFlag:
        pass
    if cmd == 'end':
        break
    taskRunFlag = True
    taskStartFlag = False
    #capture a photo with opencv
    cap = cv2.VideoCapture(0)
    ret,frame = cap.read()
    #close the camera to prevent overheat
    cap.release()
    #Undistort the image
    frame = undistort(frame)
    #Save the image to file
    fpic = open('test.jpg','w')
    cv2.imwrite('test.jpg',frame)
    fpic.close()

    #Open the transmit socket
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    packetSize = 8192
    #Get host name. This works on both windows and linux.
    try:
        #For linux
        host = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    except:
        #For windows
        host = socket.gethostname()
    
    port = 4445
    addr = ('192.168.43.1',port)

    #Prepare the file for transmittion.
    f = open("test.jpg",'rb')
    audiof = open("audio.wav",'wb')

    old_file_position = f.tell()
    f.seek(0, os.SEEK_END)
    fsize = f.tell()
    f.seek(old_file_position, os.SEEK_SET)

    fsizedata = str(fsize).encode()
    
    #Transmit photo data.
    data = f.read(packetSize)
    while data:
        if(s.sendto(data,addr)):
            data = f.read(packetSize)
        
    s.close()
    #Transmit "end"
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.sendto(b"end",addr)
    s.close()
    f.close()

    print("transmit conplete")

    #Open recieve socket
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,port))

    #Recieve audio file
    while True:
        data = s.recv(packetSize)
        if data == b'end':
            break
        else:
            audiof.write(data)
    audiof.close()
    print("receive complete")

    s.close() 

    #Extend the audio file
    extendTime(audiof.name,1)

    #Play the audio file
    call(["aplay",audiof.name])
    taskRunFlag = False

#Before quiting, play power off audio.
call(["aplay","poweroff.wav"])

try:
    cap.release()
except:
    pass