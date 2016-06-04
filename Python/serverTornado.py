import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import time
import analysisControllerTornado as aController

class WebSocketHandler(tornado.websocket.WebSocketHandler):

    # Initialize server
    # Set default permission to True
    def initialize(self):
        self.permissionStatus = True
        self.N = 4
        self.counting = []

    # This function handles new user connection
    def open(self):
        print 'New Connection'

    # This function handles incoming messages
    def on_message(self, message):
        # Decode message
        message = json.loads(message)
        msgType = message["msgType"]
        msgContent = message["msgContent"]

        # Interpret message type
        if msgType == "permissionRequest":
            self.onPermissionRequest(msgContent)
        elif msgType == "image":
            self.imageHandler(msgContent)

    # This function handles the disconnect of a client
    def on_close(self):
        print 'Connection closed'

    # This function handles the permission request
    def onPermissionRequest(self, msgContent):
        print "New permission request. Server permission status: " + str(self.permissionStatus)
        if self.permissionStatus == True:
            self.grantPermission()
        else:
            self.denyPermission()

    # This function sends a permission granted
    # If the server is ready
    def grantPermission(self):
        message = {
            "msgType": "permissionGrant",
            "msgContent": True
        }
        message = json.dumps(message)
        self.write_message(message)

    # This function sends a permission denied
    # If the server is busy
    # TODO: LATE SHOULD ADD TO REDIS QUEUE AND INFORM CLIENT
    def denyPermission(self):
        message = {
            "msgType": "permissionGrant",
            "msgContent": False
        }
        message = json.dumps(message)
        self.write_message(message)

    # This function handles an image
    # Incoming from the client
    def imageHandler(self, msgContent):
        try:
            self.permissionStatus = False
            timeStr = time.strftime("%Y%m%d-%H%M%S")
            print "New image: " + timeStr
            fileName = aController.createImage(msgContent)
            result = aController.analyseImage(fileName)
            aController.deleteImage(fileName)
            self.permissionStatus = True
            self.respondAfterAnalysis(result)
        except Exception as error:
            print "Error analysing image! Aborting"
            print error
            self.respondAfterAnalysis(True)
            self.close()

    # This function responds to a client
    # After an analysis
    def respondAfterAnalysis(self, result):
        print "Current history: " + str(self.counting)
        numberOfResults = len(self.counting)
        finalResult = False
        if numberOfResults == 0:
            self.counting.append(result)
        else:
            equalResults = 0
            for value in self.counting:
                if(value == result):
                    equalResults += 1
            if (equalResults == numberOfResults):
                self.counting.append(result)
                if(len(self.counting) == self.N and result == True):
                    finalResult = True
                    self.counting = []
                elif(len(self.counting)>self.N):
                    del self.counting[0]
            else:
                self.counting = [result]

        message = {
            "msgType": "analysisResult",
            "msgContent": finalResult
        }
        message = json.dumps(message)
        self.write_message(message)

if __name__ == '__main__':
    # Setup Server
    application = tornado.web.Application([(r'/ws', WebSocketHandler),])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()