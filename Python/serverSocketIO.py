import socketio
import eventlet
from flask import Flask
import time
# import analysisController as anc

# Define Socket.IO server and application wrapper
sio = socketio.Server()
app = Flask(__name__)

@sio.on('connect')
def connect(sid, environ):
    print 'New Connection ' + sid

@sio.on('id_request')
def id_request_handler(sid):
    print "Client: " + sid + " sent a personal ID request"
    sio.emit("register_id", sid, room = sid)

@sio.on("permission_request")
def permission_request_handler(sid):
    print "Client: " + sid + " sent a permission request"
    # check if everything id ready to receive a picture
    sio.emit("permission_granted", True, room = sid)

@sio.on("image")
def image_handler(sid, imgBase64):
    time.sleep(0.5)
    sio.emit("analysis_result", False, room = sid)

@sio.on('disconnect')
def disconnect(sid):
    print 'disconnect ' + sid

if __name__ == '__main__':
    # Wrap Flask application with Socket.IO's middleware
    app = socketio.Middleware(sio, app)
    # Deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('',5000)), app)