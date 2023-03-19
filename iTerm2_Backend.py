#!/usr/bin/env python3
import osascript
import socket
import argparse
import struct
import json
import time
def _apple_script_string_escape(s):
    tmp = repr(s)[1:-1].replace('"', '')
    return repr(tmp)[1:-1].replace('\\', '') # fix this bug


def _iterm_exec(cmd1,cmd2):
    apple_script = '''tell application "iTerm2"
    tell current session of current window
        select split vertically with default profile
        write text "{}"
        write text "{}"
    end tell
end tell
'''.format(_apple_script_string_escape(cmd1),_apple_script_string_escape(cmd2))
    osascript.run(apple_script)

def run(command1,command2):
    _iterm_exec(command1,command2)


def unpack(data):
    return struct.unpack('<I',data)

def recv(fd,size):
    buf = fd.recv(size)
    if(buf == b''):
        raise Exception
    return buf

def handle(conn:socket.socket,host,user):
    print('handle start')
    data = recv(conn,4)
    size = unpack(data)[0]
    msg = recv(conn,size)
    js = json.loads(msg)
    print(js)
    if js['terminal'] == 'iterm2':
        cmd = js['exec']
        cmd1 = f'ssh {user}@{host}'
        cmd2 = f'{cmd}'
        run(cmd1,cmd2)

def conn(host,port,user):
    addr = socket.getaddrinfo(host,port,0,0,socket.SOL_TCP)[0]
    sk = socket.socket(addr[0],addr[1],addr[2])
    host_tuple = addr[4]
    sk.connect(host_tuple)
    while True:
        data = recv(sk,5)
        print(data)
        if (data == b'heart'):
            sk.send(b'heart')
            handle(sk,host,user)
        else:
            break
    sk.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser('fake terminal that connects to outside world')
    parser.add_argument('-s', '--server', required=True, help='server host')
    parser.add_argument('-p', '--port', required=True, help='server port')
    parser.add_argument('-u', '--user', required=True, help='server user')
    args = parser.parse_args()
    host = args.server
    port = int(args.port)
    user = args.user
    while True:
        try:
            conn(host,port,user)
        except Exception as e:
            print(e)
        time.sleep(5)

        
        
  