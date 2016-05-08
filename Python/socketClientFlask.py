from socketIO_client import SocketIO
global sio

def on_response(data):
    print "O servidor disse: " + data
    # sio.emit("client_message")

if __name__ == "__main__":
    # Establish the connection
    sio = SocketIO('localhost', 5000)

    # Try to Communicate with the server
    sio.emit("client_message")
    sio.on("message_response", on_response)

    sio.wait()