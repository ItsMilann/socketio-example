import os
import socketio
from sio_app.views import sio
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')

django_application = get_wsgi_application()
application = socketio.WSGIApp(sio, django_application)
