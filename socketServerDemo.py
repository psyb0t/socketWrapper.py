#!/usr/bin/env python
from socketWrapper import TCPSocketServer

def on_start(data):
  print 'Server socket bound on {}:{} started on'.format(
    data['bind_addr'],
    data['bind_port'],
  )
  print data['socket']

def on_connect(data):
  print 'Client {}:{} connected on'.format(
    data['address'][0],
    data['address'][1]
  )
  print data['socket']

def on_disconnect(data):
  print 'Client {}:{} disconnected'.format(
    data['address'][0],
    data['address'][1]
  )

def on_receive(data):
  print 'Client {}:{} sent "{}" on'.format(
    data['client']['address'][0],
    data['client']['address'][1],
    data['data']
  )
  print data['client']['socket']

sock = TCPSocket(('127.0.0.1', 6767))

sock.on_start = on_start
sock.on_connect = on_connect
sock.on_disconnect = on_disconnect
sock.on_receive = on_receive

sock.start()