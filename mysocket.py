import socket
import time

s = socket.socket()

host = socket.gethostname()
port = 12306
s.bind((host,port))

s.listen(5)

while True:
    c,addr = s.accept()
    print("地址：",addr)
    c.send(b'Connected\n')
    print(c.recv(1024))
    
    c.close()   