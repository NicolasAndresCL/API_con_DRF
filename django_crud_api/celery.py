import os
import django
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_crud_api.settings')
django.setup()

app = Celery('django_crud_api')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(['customers.services'])
