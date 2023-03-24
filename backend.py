#!/usr/bin/env python3

import os
import socket

socketName = '/tmp/iTerm2Socket'

if(os.access(socketName,os.F_OK)):
    os.unlink(socketName)

if socket.has_ipv6:
    sk = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
    sk.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
else:
    sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

sk.bind(('', 15111))
sk.listen()

pipesk = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
pipesk.bind(socketName)
pipesk.listen()


def recv(fd,size):
    buf = fd.recv(size)
    if(buf == b''):
        raise Exception
    print(fd,b'recv',buf,len(buf))
    return buf

def send(fd,buf):
    l = fd.send(buf)
    if(l != len(buf)):
        raise Exception
    print(fd,b'send',buf,l)
    return l

def handler(conn:socket.socket,fd:socket.socket):
    while True:
        buf = recv(fd,0x100)
        print(b'buf:'+buf)
        send(conn,b'heart')
        tmp = recv(conn,5)
        if(tmp != b'heart'):
            send(fd,b'No')
            break
        send(fd,b'Yes')
        num = send(conn,buf)


while True:
    conn, addr_ = sk.accept()
    print('connect:',addr_)
    fd, addr_ = pipesk.accept()
    try:
        handler(conn,fd)
    except Exception as e:
        print(e,e.args)
    conn.close()
    fd.close()
