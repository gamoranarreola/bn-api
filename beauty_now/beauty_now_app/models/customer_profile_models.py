from django.db import models


class CustomerProfile(models.Model):
    """
    Customer profile, like a customer account.
    """

    custom_user = models.OneToOneField('CustomUser', on_delete=models.DO_NOTHING)
    customer_profile_id = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CustomerProfileAddress(models.Model):
    """
    CustomerProfileAddress model for storing user addresses.
    """
    customer_profile = models.ForeignKey(CustomerProfile, on_delete=models.DO_NOTHING)
    place_id = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)