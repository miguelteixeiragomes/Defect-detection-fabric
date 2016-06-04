import imageController as imc
import websocket
import json
import time
import sys

class WSClient():

    # Class constructor
    # Connection init
    def __init__(self, server, port):
        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp("ws://" + server + ":" + port + "/ws",
            on_message = self.on_message,
            on_error = self.on_error,
            on_close = self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()
        self.currentFileName = ""

    # This function deals with connection opening
    def on_open(self, ws):
        print "I'm connected to the server"
        self.askForPermission()

    # This function handles incoming messages
    def on_message(self, ws, message):
        # Decode message
        message = json.loads(message)
        msgType = message["msgType"]
        msgContent = message["msgContent"]

        # Interpret message type
        if msgType == "permissionGrant":
            self.onPermissionResponse(msgContent)
        elif msgType == "analysisResult":
            self.onAnalysisResultResponse(msgContent)

    # This function handles the disconnect of a client
    def on_close(self, ws):
        print "Connection closed"

    # This function handles a WebSocket error
    def on_error(self, ws, error):
        print "Socket error:" + error

    # This function asks the
    # server for permission to send an image
    def askForPermission(self):
        message = {
            "msgType": "permissionRequest",
            "msgContent": ""
        }
        message = json.dumps(message)
        self.ws.send(message)

    # This function handles the response
    # To a permission response
    def onPermissionResponse(self, msgContent):
        if msgContent == True:
            self.permissionGranted()
        else:
            time.sleep(0.25)
            self.askForPermission()

    # This function handles the case
    # Where a permission to send an image is given
    def permissionGranted(self):
        try:
            # Take picture send base64 to Server
            fileName = imc.capturePicture()
            imageBase64 = imc.convertToBase64(fileName)
            self.currentFileName = fileName
            # Send to server
            message = {
                "msgType": "image",
                "msgContent": imageBase64
            }
            message = json.dumps(message)
            self.ws.send(message)
        except Exception as error:
            print "Failed to capture image or transfer to server: " + str(error)
            self.ws.close()

    # This function handles the
    # Response to an image analysis
    def onAnalysisResultResponse(self, msgContent):
        timeStr = time.strftime("%Y%m%d-%H%M%S")
        print "New Result: " + str(msgContent) + " - " + timeStr
        print "Detection history: " + str(self.counting)
        self.resultAnalysis(msgContent)

    # This function handles the
    # Response to an image analysis
    def onAnalysisResultResponse(self, msgContent):
        timeStr = time.strftime("%Y%m%d-%H%M%S")
        print "New Result: " + str(msgContent) + " - " + timeStr
        if msgContent == True:
            self.onDefect()
        else:
            # Destroy picture - Commented for now
            # imc.deleteImage(self.currentFileName)
            self.askForPermission()

    # This function handles the case
    # Where there is a defect on the textile
    def onDefect(self):
        timeStr = time.strftime("%Y%m%d-%H%M%S")
        print "Defect detected! - " + timeStr
        print "Continuing execution"
        self.askForPermission()
        # self.ws.close()

if __name__ == "__main__":
    if (len(sys.argv) == 3):
        server = sys.argv[1]
        port = sys.argv[2]
    else:
        server = "127.0.0.1"
        port = "8888"
    client = WSClient(server, port)