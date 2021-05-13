from django.db.models import JSONField
from django.db import models
from django.db.models.fields.related import ForeignKey, ManyToManyField


class Specialty(models.Model):
    """
    Specialty model.

    Arguments:
        models {Model} -- Model class.
    """
    class Meta:
        verbose_name_plural = 'Specialties'

    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Specialty ID: {self.id} - {self.name}'


class ServiceCategory(models.Model):
    """
    Service category model.

    Arguments:
        models {Model} -- Model class.
    """
    class Meta:
        verbose_name_plural = 'Service Categories'

    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class Service(models.Model):
    """
    Service model.

    Arguments:
        models {Model} -- Model class.
    """
    service_id = models.CharField(max_length=20)
    category = ForeignKey(ServiceCategory, on_delete=models.DO_NOTHING)
    specialties = ManyToManyField(Specialty, through='ServiceSpecialty')
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    extras = models.CharField(max_length=512)
    includes_eyelashes = models.BooleanField(default=False)
    availability = JSONField()
    duration = models.TimeField()
    beautier_price = models.IntegerField()
    beauty_now_price = models.IntegerField()
    public_price = models.IntegerField()
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class ServiceSpecialty(models.Model):
    """
    Service specialty model.

    Arguments:
        models {Model} -- Model class.
    """
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING)
    specialty = models.ForeignKey(Specialty, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
