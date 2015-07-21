# socketWrapper.py

A general purpose TCP socket class.

## Installation
```
cd /path/to/script
git clone git@github.com:psyb0t/socketWrapper.py.git .
```

## Server

```
from socketWrapper import TCPSocketServer
```

The constructor accepts a tuple argument consisting of the address of the interface and the port to listen on

```
server = TCPSocketServer(('127.0.0.1', 6767))
```

### Handlers
__on_start__

Triggered right when the server successfully starts listening. Called with a dict argument of the following type:
```
data = {
    'socket': socket,
    'bind_addr': self.bind_address,
    'bind_port': self.bind_port
}
```

__on_connect__

Triggered on a successful client connection. Called with a dict argument of the following type:
```
data = {
    'socket': sock,
    'address': address
}
```

__on_disconnect__

Triggered on client disconnect. Called with a dict argument of the following type:
```
data = {
    'address': address
}
```

__on_receive__

Triggered after receiving data from the client. Called with a dict argument of the following type:
```
data = {
    'client': {
        'socket': socket,
        'address': address
    },
    'data': recv_data
}
```