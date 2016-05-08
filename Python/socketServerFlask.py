from flask import Flask
from flask_socketio import SocketIO, emit

# WebSocket configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app)


@sio.on('client_message')
def handle_my_custom_event():
    emit('message_response', "ola")

if __name__ == '__main__':
    sio.run(app)