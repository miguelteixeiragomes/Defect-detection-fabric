import socketio
import eventlet
from flask import Flask

# Define Socket.IO server and application wrapper
sio = socketio.Server()
app = Flask(__name__)

@sio.on('connect', namespace = '/test')
def connect(sid, environ):
    print 'New Connection ' + sid
    sio.emit("server_response", sid, room = sid, namespace = '/test' )

@sio.on('message', namespace = '/test')
def message(sid, data):
    print 'message ' + sid + " " + data
    sio.emit("server_reply", data = "Hello", room = sid, namespace = '/test')

@sio.on('disconnect', namespace = '/test')
def disconnect(sid):
    print 'disconnect ' + sid

if __name__ == '__main__':
    # Wrap Flask application with Socket.IO's middleware
    app = socketio.Middleware(sio, app)

    # Deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('',8000)), app)