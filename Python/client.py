from socketIO_client import SocketIO
import imageController as imc

def on_registerID(personalID):
    print "My personal register ID is: " + str(personalID)
    registerID = personalID

def on_permission(data):
    print "Server Permission: " + str(data)
    # Take picture send base64 to Server
    fileName = imc.capturePicture()
    imageBase64 = imc.convertToBase64(fileName)
    sio.emit("image", imageBase64)
    # Destroy picture
    imc.remove(fileName)

def on_kill():
    imc.killProcess()
    return True

# Establish the connection & initialize
# IP needs to be changed to correct server's IP
sio = SocketIO('192.168.3.1', 5000)

# Request for personal ID
sio.emit("id_request")
sio.on("register_id", on_registerID)

# Ask for permission to send picture and wait for the grant
sio.emit("permission_request")
sio.on("permission_granted",on_permission)
sio.on("kill_machine", on_kill)

sio.wait()
