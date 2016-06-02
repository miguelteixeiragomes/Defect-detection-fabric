import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import time

class WebSocketHandler(tornado.websocket.WebSocketHandler):

    # Initialize server
    # Set default permission to True
    def initialize(self):
        self.permissionStatus = True

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
            # TODO: Substitute for new analyser code
            time.sleep(0.5)
            result = False
            self.permissionStatus = True
            self.respondAfterAnalysis(result)
        except:
            print "Error analysing image! Aborting"
            self.respondAfterAnalysis(True)
            self.close()

    # This function responds to a client
    # After an analysis
    def respondAfterAnalysis(self, result):
        message = {
            "msgType": "analysisResult",
            "msgContent": result
        }
        message = json.dumps(message)
        self.write_message(message)

if __name__ == '__main__':
    # Setup Server
    application = tornado.web.Application([(r'/ws', WebSocketHandler),])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()