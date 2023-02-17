#!/usr/bin/python3

import argparse
import json
import struct
import socket


def pack(num):
    return struct.pack('<I', num)


def main():
    parser = argparse.ArgumentParser('fake terminal that connects to outside world')
    parser.add_argument('-e', required=True, help='execute command in outside terminal')
    parser.add_argument('-t', '--terminal', required=True, help='terminal execute command')
    args = parser.parse_args()
    cmd = args.e

    msg = {
        'exec': cmd,
        'terminal': args.terminal
    }
    msg_json = json.dumps(msg)
    length = len(msg_json)
    protocol_msg = pack(length) + msg_json.encode('latin-1')
    pipeName = '/tmp/iTerm2Socket'

    fd = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
    fd.connect(pipeName)
    while True:
        fd.send(protocol_msg)
        tmp = fd.recv(5)
        if(tmp == b'Yes'):
            break
    fd.close()

if __name__ == '__main__':
    main()