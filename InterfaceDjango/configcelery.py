# configcelery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# establecer la variable de entorno DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InterfaceDjango.settings.prod')

app = Celery('InterfaceDjango')

# Usar la configuración de Django para Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Cargar tareas desde todos los archivos registered_tasks.py en las aplicaciones de Django
app.autodiscover_tasks()
