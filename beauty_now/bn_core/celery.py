from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.contrib.admin import autodiscover

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bn_core.settings')

app = Celery(
    'beauty_now',
    broker='pyamqp://',
    backend='rpc://',
    include=['bn_core.tasks']
)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()
