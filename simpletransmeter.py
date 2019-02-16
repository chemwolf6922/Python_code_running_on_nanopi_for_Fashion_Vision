import socket

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

host = '192.168.43.89'
port = 18200

addr = (host,port)

s.sendto(b'hello',addr)
s.close()