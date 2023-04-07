#!/usr/bin/env python3

import os
import socket
import json
import time

socketName = ('172.17.0.1', 15112)

if socket.has_ipv6:
    sk = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
    sk.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
else:
    sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
sk.bind(('', 15111))
sk.listen()

pipesk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
pipesk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
pipesk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
pipesk.settimeout(5)
pipesk.bind(socketName)
pipesk.listen()

def recv(fd:socket.socket,size):
    buf = fd.recv(size)
    if(buf == b''):
        raise Exception
    return buf

def send(fd:socket.socket,buf):
    l = fd.send(buf)
    if(l != len(buf)):
        raise Exception
    return l

def checkAlive(fd:socket.socket):
    ans = False
    try:
        send(fd,b'heart')
        tmp = recv(fd,5)
        if(tmp != b'heart'):
            ans = False
        ans = True
    except:
        ans = False
    return ans

def checkCmdAlive(buf):
    try:
        buf = buf[4:]
        js = json.loads(buf)
        print('Get cmd:',js)
        now = time.time()
        old = js['time']
        print('old time:',old)
        print('now time:',now)
        print('time:',now-old)
        if(now - old >= 2):
            return False
    except :
        return False
    return True


def handler(conn:socket.socket):
    while True:
        if(not checkAlive(conn)):
            break
        try:
            fd, addr_ = pipesk.accept()
            buf = recv(fd,0x100)
            if(not checkCmdAlive(buf)):
                continue
            send(conn,b'handl')
            send(conn,buf)
        except:
            continue

while True:
    conn, addr_ = sk.accept()
    conn.settimeout(5)
    print('connect:',addr_)
    try:
        handler(conn)
    except Exception as e:
        print(e,e.args)
    print('disconnect:',addr_)
    conn.close()
