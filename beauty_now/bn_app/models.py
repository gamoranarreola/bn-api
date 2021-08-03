from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models import JSONField, constraints
from django.db import models

from .managers import AuthUserManager


class AuthUser(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(unique=True, max_length=128)
    phone = models.CharField(max_length=64, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AuthUserManager()

    def __str__(self):
        return f'{self.last_name}, {self.first_name} ({self.email})'


class CustomerProfile(models.Model):

    auth_user = models.OneToOneField('AuthUser', on_delete=models.DO_NOTHING)
    customer_profile_id = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.__dict__}'


class CustomerProfileAddress(models.Model):

    customer_profile = models.ForeignKey(CustomerProfile, on_delete=models.DO_NOTHING)
    place_id = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.__dict__}'


class BeautierProfile(models.Model):

    auth_user = models.OneToOneField('AuthUser', on_delete=models.DO_NOTHING)
    specialties = models.ManyToManyField('Specialty')
    calendar_id = models.CharField(max_length=128, null=True)
    availability = JSONField(default=dict)


class Specialty(models.Model):

    class Meta:
        verbose_name_plural = 'Specialties'

    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Specialty ID: {self.id} - {self.name}'


class ServiceCategory(models.Model):

    class Meta:
        verbose_name_plural = 'Service Categories'

    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class Service(models.Model):

    service_id = models.CharField(max_length=20)
    category = models.ForeignKey('ServiceCategory', on_delete=models.DO_NOTHING)
    specialties = models.ManyToManyField('Specialty')
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


class WorkOrder(models.Model):

    request_date = models.CharField(null=True, max_length=10)
    request_time = models.CharField(null=True, max_length=8)
    place_id = models.CharField(max_length=128, null=True)
    customer_profile = models.ForeignKey('CustomerProfile', on_delete=models.DO_NOTHING)
    line_items = models.ManyToManyField('LineItem')
    notes = models.CharField(max_length=256, blank=True)
    status = models.CharField(max_length=32, default='initial_request')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.__dict__}'


class LineItem(models.Model):

    service = models.ForeignKey('Service', on_delete=models.DO_NOTHING)
    service_date = models.CharField(null=True, max_length=10)
    service_time = models.CharField(null=True, max_length=8)
    quantity = models.IntegerField()
    price = models.IntegerField(default=0)
    staffing_assignments = models.ManyToManyField('StaffingAssignment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.__dict__}'


class StaffingAssignment(models.Model):

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['line_item', 'index'], name='line_item_index')
        ]

    line_item = models.ForeignKey('LineItem', on_delete=models.DO_NOTHING)
    index = models.IntegerField()
    beautier_profiles = models.ManyToManyField('BeautierProfile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.__dict__}'
