from django.core.management.commands.runserver import Command as RunCommand

from sio_app.views import sio


class Command(RunCommand):
    help = 'Run the Socket.IO server'

    def handle(self, *args, **options):
        print("Runnning Custom Command")
        if sio.async_mode == 'threading':
            super(Command, self).handle(*args, **options)
        elif sio.async_mode == 'eventlet':
            # deploy with eventlet
            import eventlet
            import eventlet.wsgi
            from webapp.wsgi import application
            eventlet.wsgi.server(eventlet.listen(('', 8000)), application)
        elif sio.async_mode == 'gevent':
            # deploy with gevent
            from gevent import pywsgi
            from webapp.wsgi import application
            try:
                from geventwebsocket.handler import WebSocketHandler
                websocket = True
            except ImportError:
                websocket = False
            if websocket:
                pywsgi.WSGIServer(
                    ('', 8000), application,
                    handler_class=WebSocketHandler).serve_forever()
            else:
                pywsgi.WSGIServer(('', 8000), application).serve_forever()
        elif sio.async_mode == 'gevent_uwsgi':
            print('Start the application through the uwsgi server. Example:')
            print('uwsgi --http :5000 --gevent 1000 --http-websockets '
                  '--master --wsgi-file webapp/wsgi.py --callable '
                  'application')
        else:
            print('Unknown async_mode: ' + sio.async_mode)
