import socketio
import random


sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': './public/'
})

count = 0
group_a = 0
group_b = 0

# def callback(data):
#     print(data)

def task(sid):
    sio.sleep(5)
    # sio.emit('mult', {'numbers': [3,4]}, callback=callback)
    res = sio.call('mult', {'numbers': [3,4]}, to=sid)
    print(res)


@sio.event
def connect(sid, environ):
    global count
    global group_b
    global group_a
    count += 1
    # getting values from headers
    username = environ.get('HTTP_X_USERNAME')
    print("USERNAME", username)
    if username == None:
        return False
    # storing values to session
    with sio.session(sid) as session:
        session['username'] = username
    # broadcasting user has joined
    sio.emit('user_joined', username)
    sio.start_background_task(task, sid)
    if random.random() > 0.5:
        sio.enter_room(sid, 'b')
        group_b += 1
        sio.emit('room_count', ['Group B', group_b], to='b' )
    else:
        sio.enter_room(sid, 'a')
        group_a += 1
        sio.emit('room_count', ['Group A', group_a], to='a' )
    sio.emit('count', count )


@sio.event
def disconnect(sid):
    global count
    global group_b
    global group_a
    count -= 1
    if 'a' in sio.rooms(sid):
        group_a -= 1
        sio.emit('room_count', ['Group A', group_a], to='a' )
    if 'b' in sio.rooms(sid):
        group_b -= 1
        sio.emit('room_count', ['Group B', group_b], to='b' )
    sio.emit('count', count)
    with sio.session(sid) as session:
        username = session['username'] # get value from session
        sio.emit('user_left', session['username'])
    print(sid, 'disconnected')


@sio.event
def text(sid, data):
    print(data)
    sio.emit('message', {'message': data})
