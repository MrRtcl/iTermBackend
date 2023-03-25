#!/usr/bin/env python3

import json
import struct
import socket
import os
import sys

def pack(num):
    return struct.pack('<I', num)


def main():
    if (len(sys.argv)==1):
        path = os.path.abspath(os.curdir)
    else:
        path = os.path.abspath(sys.argv[1])
    msg = {
        'type': 'code',
        'path': path
    }
    msg_json = json.dumps(msg)
    length = len(msg_json)
    protocol_msg = pack(length) + msg_json.encode('latin-1')
    pipeName = '/tmp/iTerm2Socket'
    fd = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
    fd.connect(pipeName)
    fd.send(protocol_msg)
    fd.close()

if __name__ == '__main__':
    main()
