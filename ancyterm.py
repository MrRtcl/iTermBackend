#!/usr/bin/env python3

import argparse
import json
import struct
import socket
import os
import time

def pack(num):
    return struct.pack('<I', num)


def main():
    parser = argparse.ArgumentParser('fake terminal that connects to outside world')
    parser.add_argument('-e', required=True, help='execute command in outside terminal')
    args = parser.parse_args()
    cmd = args.e

    msg = {
        'type': 'gdb',
        'exec': cmd,
        'path': os.path.abspath(os.curdir),
        'time': time.time()
    }
    msg_json = json.dumps(msg)
    length = len(msg_json)
    protocol_msg = pack(length) + msg_json.encode('latin-1')
    pipeName = ('172.17.0.1',15112)
    fd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    fd.connect(pipeName)
    fd.send(protocol_msg)
    fd.close()

if __name__ == '__main__':
    main()