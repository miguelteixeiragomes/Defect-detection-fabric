from socketIO_client import SocketIO
import time

def on_registerID(personalID):
    print "My personal register ID is: " + str(personalID)
    registerID = personalID

def on_permission(data):
    print data
    # Take picture send base64 to Server
    imageBase64 = "123"
    sio.emit("image", imageBase64)

def on_close():
    print "Fuck this"

# Establish the connection & initialize
sio = SocketIO('localhost', 5000)

sio.emit("id_request")
sio.on("register_id", on_registerID)

# Ask for permission to send picture and wait for the grant
sio.emit("permission_request")
sio.on("permission_granted",on_permission)
sio.on("kill_machine", on_close)

sio.wait()