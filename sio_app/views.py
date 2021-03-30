import os
import socketio
from django.shortcuts import render


sio = socketio.Server(async_mode='eventlet')
thread = None

def index(request):
    return render(request, 'sio_app/index.html')


@sio.event
def connect(sid, environ):
    username = environ.get('HTTP_X_USERNAME')
    print("USERNAME", username)
    if username == None:
        return False
    with sio.session(sid) as session:
        session['username'] = username
    sio.emit('user_joined', username)


@sio.event
def disconnect(sid):
    with sio.session(sid) as session:
        username = session['username']
        sio.emit('user_left', session['username'])

@sio.event
def text(sid, data):
    sio.emit('message', {'message': data})
