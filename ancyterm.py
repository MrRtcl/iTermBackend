#!/usr/bin/env python3

import argparse
import json
import struct
import socket
import os

def pack(num):
    return struct.pack('<I', num)


def main():
    parser = argparse.ArgumentParser('fake terminal that connects to outside world')
    parser.add_argument('-e', required=True, help='execute command in outside terminal')
    args = parser.parse_args()
    cmd = args.e

    msg = {
        'exec': cmd,
        'path': os.path.abspath(os.curdir)
    }
    msg_json = json.dumps(msg)
    length = len(msg_json)
    protocol_msg = pack(length) + msg_json.encode('latin-1')
    pipeName = '/tmp/iTerm2Socket'
    fd = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
    fd.connect(pipeName)
    fd.send(protocol_msg)
    tmp = fd.recv(5)
    if(tmp == b'No'):
        print('Connection error.Please check client.')
    fd.close()

if __name__ == '__main__':
    main()