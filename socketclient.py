import socket               # 导入 socket 模块

s = socket.socket()         # 创建 socket 对象
host = '192.168.137.1' # 获取本地主机名
port = 12306                # 设置端口号

s.connect((host, port))
print(s.recv(1024))
s.send(b'123')
s.close()  