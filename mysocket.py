import socket
import time

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


host = socket.gethostname()
port = 4445
s.bind((host,port))

data,addr = s.recvfrom(1024)
s.sendto(b"revieved\n",addr)

print(data)

s.close() 