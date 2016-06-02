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
        self.ws = websocket.WebSocketApp("ws://127.0.0.1:8888/ws",
            on_message = self.on_message,
            on_error = self.on_error,
            on_close = self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()

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

    # This function
    def onPermissionResponse(self, msgContent):
        if msgContent == True:
            self.permissionGranted()
        else:
            time.sleep(0.25)
            self.askForPermission()

    # This function
    def permissionGranted(self):
        # Take picture send base64 to Server
        fileName = imc.capturePicture()
        imageBase64 = imc.convertToBase64(fileName)
        # Destroy picture - Commented for now
        # imc.deleteImage(fileName)
        # Send to server
        message = {
            "msgType": "image",
            "msgContent": imageBase64
        }
        message = json.dumps(message)
        self.ws.send(message)

    # This function
    def onAnalysisResultResponse(self, msgContent):
        timeStr = time.strftime("%Y%m%d-%H%M%S")
        print "New Result: " + msgContent + " - "  + timeStr
        if msgContent == True:
            self.onDefect()
        else:
            self.askForPermission()

    # This function
    def onDefect(self):
        print "Defect detected! Closing down system"
        self.ws.close()

if __name__ == "__main__":
    # TODO: sys.argv
    client = WSClient("172.0.0.1", "8888")