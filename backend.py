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
pipesk.settimeout(5)
pipesk.bind(socketName)
pipesk.listen()

def recv(fd:socket.socket,size):
    buf = fd.recv(size)
    if(buf == b''):
        raise Exception
    print(fd.family,b'recv',buf,len(buf))
    return buf

def send(fd:socket.socket,buf):
    l = fd.send(buf)
    if(l != len(buf)):
        raise Exception
    print(fd.family,b'send',buf,l)
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


def handler(conn:socket.socket):
    while True:
        if(not checkAlive(conn)):
            break
        try:
            fd, addr_ = pipesk.accept()
            buf = recv(fd,0x100)
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
