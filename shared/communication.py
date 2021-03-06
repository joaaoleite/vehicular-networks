import socket
import json
from time import time
from threading import Thread

import struct

PORT = 4173

session = None


def binding():
    global session
    session.bind(('', PORT, 0, 2))


def setup_its():
    global session
    print "creating socket..."
    session = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    thread = Thread(target=binding, args=())
    thread.start()


def setup():
    global session
    print "creating socket..."
    session = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    session.bind(('', PORT, 0, 2))
    session.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, socket.inet_pton(socket.AF_INET6, "ff02::1")+'\0'*4)
    session.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 5)


def send(msg, ip):
    if ip == "all":
        ip = "ff02::1%wlan0"
    msg = json.dumps(msg)
    print msg
    try:
        session.sendto(msg, (ip, PORT))
    except Exception,e:
        print e
        print 'error sending message'


def receive():
    data, address = session.recvfrom(100000)
    data = json.loads(data)

    #if int(time()) - int(data['time']) > 60:
    #    return None
    #else:
    return data


def shutdown():
    global session
    print 'closing socket...'
    try:
        session.shutdown(socket.SHUT_RDWR)
    except socket.error:
        print 'Close socket'
