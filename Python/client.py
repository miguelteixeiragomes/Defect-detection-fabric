from socketIO_client import SocketIO
import imageController as imc
import sys

# This function handles the permission requests and responses
def askForPermission():
    sio.emit("permission_request")
    sio.on("permission_granted", onPermisisonResponse)
    
# This function handles the process abortion
def abortProcess():
    print "Aborting process"
    sio.emit("disconnect")
    imc.killProcess()
    sys.exit("Process aborted")

# This function is the callback for an image analysis request
# In case there is NO DEFFECT, asks for permission to send another image
# In case there IS A DEFFECT, aborts the process
def imageAnalysisResponse(result):
    print "Este foi o resultado da analise: " + str(result)
    if (result == False):
        askForPermission()
    else:
        abortProcess()
        
# This function handles the ID request response
def on_registerID(personalID):
    print "My personal register ID is: " + str(personalID)
    registerID = personalID

# This function handles the permission granted response
# Prepares the image data and sends it to the server
# Waits for response callback
def onPermisisonResponse(data):
    print "Server Permission: " + str(data)
    # Take picture send base64 to Server
    fileName = imc.capturePicture()
    imageBase64 = imc.convertToBase64(fileName)
    # Destroy picture - Commented for now
    #imc.deleteImage(fileName)
    # Send to server
    sio.emit("image", imageBase64)
    sio.on("analysis_result", imageAnalysisResponse)

if __name__ == "__main__":
    try:
        # Establish the connection & initialize
        # IP is set to Gil's mac
        sio = SocketIO('192.168.1.10', 5000)
        # Request for personal ID
        sio.emit("id_request")
        sio.on("register_id", on_registerID)
        print "I'm registered on the server"
        # Ask for permission
        askForPermission()
        # Wait for response
        sio.wait()
    except KeyboardInterrupt:
        # User interrupted, abort process
        print "Abort by user interrupt"
        abortProcess()
    
