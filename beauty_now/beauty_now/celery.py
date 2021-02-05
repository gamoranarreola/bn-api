from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.contrib.admin import autodiscover

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beauty_now.settings')

app = Celery(
    'beauty_now',
    broker='pyamqp://',
    backend='rpc://',
    include=['beauty_now.tasks']
)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()
