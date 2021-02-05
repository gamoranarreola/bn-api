from django.db import models

from .beautier_models import BeautierProfile
from .service_models import Service
from .customer_profile_models import CustomerProfile


class WorkOrder(models.Model):
    """
    Work order model.
    
    Arguments:
        models {Model} -- Model class.
    """
    request_date = models.CharField(null=True, max_length=10)
    request_time = models.CharField(null=True, max_length=8)
    customer_profile = models.ForeignKey(CustomerProfile, on_delete=models.DO_NOTHING)
    place_id = models.CharField(max_length=128, null=True)
    notes = models.CharField(max_length=256, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.__dict__}'


class LineItem(models.Model):
    """
    Line item model.
    
    Arguments:
        models {Model} -- Model class.
    """
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING)
    service_date = models.CharField(null=True, max_length=10)
    service_time = models.CharField(null=True, max_length=8)
    quantity = models.IntegerField()
    price = models.IntegerField(default=0)
    status = models.CharField(max_length=32, default='initial_request')
    beautier_profile = models.ForeignKey(BeautierProfile, null=True, default=None, on_delete=models.DO_NOTHING)
    work_order = models.ForeignKey(WorkOrder, related_name='line_items', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.__dict__}'
