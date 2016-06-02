import websocket
import httplib
import sys
import asyncore

def connect(server, port):
    # Inform connection settings
    print("connecting to: %s:%d" %(server, port))

    # Perform handshake with server and get respective values
    conn = httplib.HTTPConnection(server + ":" + str(port))
    conn.request("POST", "/socket.io/1/")
    resp = conn.getresponse()
    hskey = resp.read().split(":")[0]

    # Init socket and event listening
    ws = websocket.WebSocket(
        "ws://" + server + ":" + str(port) + "/socket.io/1/websocket/" + hskey,
        # event1 = handler1,
        # event2 = handler2,
        # event3 = handler3,
    )

    return ws

if __name__ == "__main__":
    # Define server settings
    server = "172.16.1.100"
    port = 5000

    # Init connection
    ws = connect(server. port)

    try:
        # Loop listening
        asyncore.loop()
    except Exception as error:
        # Close on error
        print "Aborting program. Cause: " + str(error)
        ws.close()