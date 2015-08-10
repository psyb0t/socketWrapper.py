import select
import socket
import sys

from time import localtime, gmtime, time, strftime

class TCPSocketServer:
  def __init__(self, bind_opt):
    if type(bind_opt) is not tuple:
      self.output(('FATAL', 'Invalid bind_opt type. Tuple expected'))
    
    self.bind_addr, self.bind_port = bind_opt
    try:
      self.bind_port = int(self.bind_port)
    except:
      self.output(('FATAL', 'Invalid bind port type'))
    
    self.connections = []
  
  def start(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((self.bind_addr, self.bind_port))
    s.listen(1)
    
    data = {
      'socket': s,
      'bind_addr': self.bind_addr,
      'bind_port': self.bind_port
    }
    self.on_start(data)
    
    self.connections.append(s)
    while True:
      readable, writable, errored = select.select(self.connections, [], [])
      
      for r in readable:
        if r is s:
          sock, address = s.accept()
          self.connections.append(sock)
          
          data = {
            'socket': sock,
            'address': address
          }
          
          self.on_connect(data)
        else:
          recv_data = []
          address = r.getpeername()
          
          while True:
            try:
              r.setblocking(0)
              data = r.recv(512)
              if data:
                recv_data.append(data)
              else:
                self.remove_connection(r)
            except:
              break
          
          if len(recv_data) > 0:
            data = {
              'client': {
                'socket': r,
                'address': address
              },
              'data': ''.join(recv_data).strip()
            }
            
            self.on_receive(data)
  
  def remove_connection(self, conn):
    try:
      address = conn.getpeername()
      conn.close()
      self.connections.remove(conn)
      
      data = {
        'address': address
      }
      
      self.on_disconnect(data)
    except:
      pass
  
  def on_start(self, data):
    pass
  
  def on_connect(self, data):
    pass
  
  def on_disconnect(self, data):
    pass
  
  def on_receive(self, data):
    pass
  
  def output(self, data):
    oType, oMessage = data
    if oType in ['INFO', 'WARN', 'FATAL']:
      print '{} [{}] {}'.format(
        strftime("%Y %m %d %H:%M:%S", localtime()),
        oType, oMessage
      )
      
      if oType is 'FATAL':
        sys.exit()

class TCPSocketClient:
  def __init__(self, conn_opt):
    if type(conn_opt) is not tuple:
      self.output(('FATAL', 'Invalid conn_opt type. Tuple expected'))
    
    self.conn_addr, self.conn_port = conn_opt
    try:
      self.conn_port = int(self.conn_port)
    except:
      self.output(('FATAL', 'Invalid connect port type'))
  
  def start(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
      s.connect((self.conn_addr, self.conn_port))
    except:
      self.on_conn_err('could not connect to server at %s:%s' % (
        self.conn_addr, self.conn_port
      ))
    
    data = {
      'socket': s,
      'address': (self.conn_addr, self.conn_port)
    }
    self.on_connect(data)
    
    connections = [s]
    while True:
      readable, writable, errored = select.select(connections, [], [])
      
      for r in readable:
        if r is s:
          recv_data = []
          while True:
            try:
              r.setblocking(0)
              data = r.recv(512)
              if data:
                recv_data.append(data)
              else:
                self.on_disconnect(r)
            except:
              break
          
          if len(recv_data) > 0:
            address = r.getpeername()
            
            data = {
              'server': {
                'socket': r,
                'address': address
              },
              'data': ''.join(recv_data).strip()
            }
            
            self.on_receive(data)
  
  def on_connect(self, data):
    pass
  
  def on_conn_err(self, data):
    pass
  
  def on_receive(self, data):
    pass
  
  def on_disconnect(self, data):
    pass
  
  def output(self, data):
    oType, oMessage = data
    if oType in ['INFO', 'WARN', 'FATAL']:
      print '{} [{}] {}'.format(
        strftime("%Y %m %d %H:%M:%S", localtime()),
        oType, oMessage
      )
      
      if oType is 'FATAL':
        sys.exit()