#!/usr/bin/env python
import socket,urllib2,sys
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind(("",8888))
sock.listen(5)

def recvall(sock):
    data = sock.recv(1024)
    while True:
        data2 = sock.recv(1024)
        if not len(data2):
            break
        data += data2
    return data

while True:
    try:
        conn,addr = sock.accept()
        conn.settimeout(10)
        data = recvall(conn)
        print data
        conn.close()
        break

    except KeyboardInterrupt:
            sock.close()
            break

