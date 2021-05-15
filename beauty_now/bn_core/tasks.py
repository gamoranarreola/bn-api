from __future__ import absolute_import, unicode_literals

import os.path
from datetime import datetime
import locale

from django.core.mail import send_mail
from django.template.loader import get_template

from bn_app.models import AuthUser, Service

from .celery import app
from .settings import EMAIL_HOST_USER

# locale.setlocale(locale.LC_TIME, 'es_MX.UTF-8')

@app.task
def handle_initial_work_order_request(auth_user_id, work_order, formatted_address):

    auth_user = AuthUser.objects.get(pk=auth_user_id)
    service = Service.objects.get(pk=work_order.get('line_items')[0]['service_id'])
    request_date = datetime.strptime(work_order.get('request_date'), '%Y-%m-%d')
    service_date = datetime.strptime(work_order.get('service_date'), '%Y-%m-%d')

    context = {
        'client_name': f'{auth_user.last_name}, {auth_user.first_name}',
        'service_address': formatted_address,
        'email': auth_user.email,
        'phone': auth_user.phone,
        'request_date': request_date.strftime('%A %e %B %Y'),
        'request_time': work_order.get('request_time'),
        'service_date': service_date.strftime('%A %e %B %Y'),
        'service_time': work_order.get('service_time'),
        'service': service.name,
        'quantity': work_order.get('line_items')[0]['quantity'],
        'price': work_order.get('line_items')[0]['price']
    }

    _email_initial_work_order_request_admin(context)
    _email_initial_work_order_request_customer(context)


def _email_initial_work_order_request_admin(context):

    template = get_template('initial_work_order_request_admin.html')
    content = template.render(context)

    send_mail(
        'BEAUTY NOW - Nueva Orden de Trabajo',
        None,
        'registro@beautynow.mx',
        ['g.a.moran.arreola@gmail.com'],
        fail_silently=False,
        html_message=content
    )


def _email_initial_work_order_request_customer(context):

    template = get_template('initial_work_order_request_customer.html')
    content = template.render(context)

    send_mail(
        'BEAUTY NOW - Nueva Orden de Trabajo',
        None,
        'registro@beautynow.mx',
        [context['email']],
        fail_silently=False,
        html_message=content
    )
