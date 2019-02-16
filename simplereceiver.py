import socket

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

host = socket.gethostname()
port = 9876

addr = (host,port)
s.bind(addr)
while True:
    data = s.recv(1024)
    print(data)