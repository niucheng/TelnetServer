#!/usr/bin/env python
# coding: utf-8

"""Telnet server

Yet another telnet server implemented via Python. Enjoy!
"""

import datetime
import socket
import threading

__version__ = '0.0.1 build %s' % '20140822'

welcome_slogan = '''Welcome novice!
Type something and hit enter to see what happens.
Be bold!

'''
help_message = '''Command         Description
===============================================================
HELP            Print this help message
WHO             List user(s) online
TALK 'MESSAGE'  Talk to other user(s) in the same telnet system
EXIT            Quit the telnet service

At your service.  Telnet server application. Version: %s

''' % __version__
goodbye_farewell = '''Have a lot of fun!'''

PS1 = 'TELNET# '

HOST = ''
PORT = 56789

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
clients = []  # list of clients connected
lock = threading.Lock()


class TelnetServer(threading.Thread):
    def __init__(self, bind):
        threading.Thread.__init__(self)
        (self.socket, self.address) = bind

    @staticmethod
    def puts(string, end='\n'):
        t = datetime.datetime.now().strftime('%c')
        print string % t, end,
        return t

    def run(self):
        lock.acquire()
        clients.append(self)
        lock.release()
        self.puts('+ %s %s connected.' % ('%s', '%s:%s' % self.address))
        self.socket.send(welcome_slogan.replace('\n', '\r\n').encode())
        while True:
            self.socket.send(PS1.encode())
            data = self.socket.recv(1024)
            temp = data.decode().strip()
            if not data:
                break
            elif temp.startswith('#') or temp == '':
                pass
            elif temp.upper() in ['BY', 'BYE', 'QUIT', 'EXIT']:
                break
            elif temp.lower() in ['?', 'help']:
                self.socket.send(help_message.replace('\n', '\r\n').encode())
            elif temp[:5].lower() == 'talk ':
                t = self.puts('> %s %s says: %s' % (self.address, '%s', temp[5:]))
                for c in clients:
                    c.socket.send(('%s %s says: %s\r\n' % (self.address, t, temp[5:])).encode())
            elif temp.lower() in ['w', 'who', 'list']:
                t = self.puts('* %s %s %s' % (self.address, '%s', 'lists user(s) online.'))
                c = []
                for n, x in enumerate(clients):
                    c.append(x.address)
                self.socket.send(('%s\r\n%s\r\n%s\r\n' % (t, '%s user(s) online' % len(clients), c)).encode())
            else:
                self.socket.send(data)
        self.socket.send(goodbye_farewell.replace('\n', '\r\n').encode())
        self.socket.close()
        self.puts('- %s %s disconnected.' % ('%s', '%s:%s' % self.address))
        lock.acquire()
        clients.remove(self)
        lock.release()


while True:  # wait for socket to connect
    # send socket to telnet server and start monitoring
    TelnetServer(s.accept()).start()
