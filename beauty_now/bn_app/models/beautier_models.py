from django.db.models import JSONField
from django.db import models

from .service_models import Specialty
from .user_models import CustomUser


class BeautierProfile(models.Model):
    """Beautier model."""
    custom_user = models.OneToOneField(CustomUser, on_delete=models.DO_NOTHING)
    specialties = models.ManyToManyField(Specialty, through='BeautierProfileSpecialty')
    calendar_id = models.CharField(max_length=128, null=True)
    availability = JSONField(default=dict)


class BeautierProfileSpecialty(models.Model):
    """
    Beautier specialty model.

    Arguments:
        models {Model} -- Model class.
    """
    class Meta:
        verbose_name_plural = 'Beautier Specialties'

    beautier_profile = models.ForeignKey(BeautierProfile, on_delete=models.DO_NOTHING)
    specialty = models.ForeignKey(Specialty, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Beautier Profile ID: {self.beautier_profile.id} - Specialty ID: {self.specialty.id} {self.specialty.name}'
