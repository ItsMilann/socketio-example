import socketio
'''
Changing to async server:
`async_mode='asgi': `
'''
sio = socketio.AsyncServer(async_mode="asgi")
app = socketio.ASGIApp(sio, static_files={
    '/': './public/'
})


@sio.event
async def connect(sid, environ):
    print(sid, 'connected')


@sio.event
async def disconnect(sid):
    print(sid, 'disconnected')


@sio.event
async def add(sid, data):
    result = sum(data['numbers'])
    await sio.emit('sum_results', {'result': result}, to=sid)
