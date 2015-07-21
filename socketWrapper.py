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
    
    self.readable_list = []
  
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
    self.readable_list = [s]
    while True:
      readable, writable, errored = select.select(self.readable_list, [], [])
      
      for r in readable:
        if r is s:
          sock, address = s.accept()
          self.readable_list.append(sock)
          
          data = {
            'socket': sock,
            'address': address
          }
          
          self.on_connect(data)
        else:
          recv_data = []
          while True:
            try:
              r.setblocking(0)
              data = r.recv(1)
              if data:
                recv_data.append(data)
              else:
                self.remove_connection(r)
            except:
              break
          
          if len(recv_data) > 0:
            address = r.getpeername()
            
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
      self.readable_list.remove(conn)
      
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
