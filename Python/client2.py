import websocket
import httplib
import sys
import asyncore

def connect(server, port):

    # Example in functional
    def _on_cenas_func(cenas):
        print cenas

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

# Def example
def _on_cenas(ws, cenas):
    print cenas

if __name__ == "__main__":
    # Define server settings
    if (len(sys.argv) == 3):
        # Case user specified
        server = sys.argv[1]
        port = int(sys.argv[2])
    else:
        # Use default to connect to Gil's mac
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