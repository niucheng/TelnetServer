TelnetServer
============

Telnet server application implementation via Python.

Server
------

```
$ python TelnetServer.py
+ Sat Aug 23 00:37:33 2014 127.0.0.1:52013 connected.
* ('127.0.0.1', 52013) Sat Aug 23 00:37:58 2014 lists user(s) online.
> ('127.0.0.1', 52013) Sat Aug 23 00:38:06 2014 says: Hi there!
- Sat Aug 23 00:38:08 2014 127.0.0.1:52013 disconnected.
```

Client
------

```
$ telnet localhost 56789
Trying ::1...
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
Welcome novice!
Type something and hit enter to see what happens.
Be bold!

TELNET# ?
Command         Description
===============================================================
HELP            Print this help message
WHO             List user(s) online
TALK 'MESSAGE'  Talk to other user(s) in the same telnet system
EXIT            Quit the telnet service

At your service.  Telnet server application. Version: 0.0.1 build 20140822

TELNET# w
Sat Aug 23 00:37:58 2014
1 user(s) online
[('127.0.0.1', 52013)]
TELNET# talk Hi there!
('127.0.0.1', 52013) Sat Aug 23 00:38:06 2014 says: Hi there!
TELNET# by
Have a lot of fun!Connection closed by foreign host.
```

Have a lot of fun! :sparkles:

