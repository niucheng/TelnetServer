#!/usr/bin/env python
# coding: utf-8

import socket
import threading

welcome_slogan = '''Welcome novice!\r\n\
Type something and hit enter to see what happens.\r\n\
Be bold!\r\n\r\n'''
help_message = '''Command         Description\r\n\
=============================================================\r\n\
HELP            Print this help message\r\n\
TALK 'MESSAGE'  Talk to other users in the same telnet system\r\n\
EXIT            Quit the telnet service\r\n\r\n\
At your service. 20140819\r\n\r\n'''
goodbye_farewell = '''Have a lot of fun!\r\n'''

PS1 = 'TELNET# '

HOST = ''
PORT = 56789

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
clients = []  # list of clients connected
lock = threading.Lock()


class telnetServer(threading.Thread):
    def __init__(self, bind):
        threading.Thread.__init__(self)
        (self.socket, self.address) = bind

    def run(self):
        lock.acquire()
        clients.append(self)
        lock.release()
        print ('+ %s:%s connected.' % self.address)
        self.socket.send(welcome_slogan.encode())
        while True:
            self.socket.send(PS1.encode())
            data = self.socket.recv(1024)
            temp = data.decode().strip()
            if not data:
                break
            elif temp.upper() in ['BY', 'BYE', 'QUIT', 'EXIT']:
                break
            elif temp.lower() in ['?', 'help']:
                self.socket.send(help_message.encode())
            elif temp.startswith('#') or temp == '':
                pass
            elif temp[:5].upper() == 'TALK ':
                print ('%s %s' % (self.address, temp[5:]))
                for c in clients:
                    c.socket.send(('%s %s\r\n' % (self.address, temp[5:])).encode())
            else:
                self.socket.send(data)
        self.socket.send(goodbye_farewell.encode())
        self.socket.close()
        print ('- %s:%s disconnected.' % self.address)
        lock.acquire()
        clients.remove(self)
        lock.release()

while True:  # wait for socket to connect
    # send socket to telnetserver and start monitoring
    telnetServer(s.accept()).start()

