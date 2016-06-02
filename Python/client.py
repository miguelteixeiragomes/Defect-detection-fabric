from socketIO_client import SocketIO
import imageController as imc
import sys

class SocketIOClient(SocketIO):
    def _should_stop_waiting(self, for_connect=False, for_callbacks=False):
        if for_connect:
            for namespace in self._namespace_by_path.values():
                is_namespace_connected = getattr(
                    namespace, '_connected', False)
                #Added the check and namespace.path
                #because for the root namespaces, which is an empty string
                #the attribute _connected is never set
                #so this was hanging when trying to connect to namespaces
                # this skips the check for root namespace, which is implicitly connected
                if not is_namespace_connected and namespace.path:
                    return False
            return True
        if for_callbacks and not self._has_ack_callback:
            return True
        return super(SocketIO, self)._should_stop_waiting()

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
        if (len(sys.argv) == 3):
            server = sys.argv[1]
            port = int(sys.argv[2])
        else:
            # TODO: Change to Gil's mac
            server = "127.0.0.1"
            port = 5000
        sio = SocketIOClient(server, port)
        # Request for personal ID
        sio.emit("id_request")
        sio.on("register_id", on_registerID)
        print "I'm registered on the server"
        # Ask for permission
        askForPermission()
        # Wait for response
        sio.wait()
    except Exception as error:
        # Error or user interrupt
        print "Abort by user error or interrupt: " + str(error)
        abortProcess()
    
