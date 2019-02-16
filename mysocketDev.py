import cv2
import socket
import time
import os
import openal as al
import netifaces as ni

cap = cv2.VideoCapture(0)
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

print(host)

port = 4445


addr = ('192.168.43.1',port)

print(addr)

startTime = time.time()


f = open("test.jpg",'rb')
audiof = open("audio.wav",'wb')

old_file_position = f.tell()
f.seek(0, os.SEEK_END)
fsize = f.tell()
f.seek(old_file_position, os.SEEK_SET)

fsizedata = str(fsize).encode()
print(fsizedata)

data = f.read(packetSize)
while data:
    if(s.sendto(data,addr)):
        data = f.read(packetSize)
    
s.close()
#time.sleep(0.1)
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

print(time.time()-startTime)

s.close() 

source = al.oalOpen(audiof.name)

source.play()
while source.get_state() == al.AL_PLAYING:
    pass
al.oalQuit()

cap.release()