from socketIO_client import SocketIO, BaseNamespace
global sio
global testNamespace
global myId

class testNamespace(BaseNamespace):

    def on_server_response(self, userID):
        myId = userID
        print "Socket connection accepted"
        print "I was assigned the id: " + myId

    def on_server_reply(self, data):
        print "message response: " + data

if __name__ == "__main__":
    # Establish the connection
    sio = SocketIO('localhost', 8000)
    testNamespace = sio.define(testNamespace, '/test')

    print "Going to emit message"
    testNamespace.emit("message", "Hello")

    sio.wait()