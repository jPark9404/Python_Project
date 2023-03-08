import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'harmony_web.settings')
app = Celery('harmony_web')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
