from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import JSONField

from .managers import AuthUserManager


class AuthUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name_plural = "Auth Users"

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(unique=True, max_length=128)
    phone = models.CharField(max_length=64, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AuthUserManager()

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.email})"


class CustomerProfile(models.Model):
    class Meta:
        verbose_name_plural = "Customer Profiles"

    auth_user = models.OneToOneField("AuthUser", on_delete=models.DO_NOTHING)
    customer_profile_id = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.__dict__}"


class CustomerProfileAddress(models.Model):
    class Meta:
        verbose_name_plural = "Customer Profile Addresses"

    customer_profile = models.ForeignKey(CustomerProfile, on_delete=models.DO_NOTHING)
    place_id = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.__dict__}"


class BeautierProfile(models.Model):
    class Meta:
        verbose_name_plural = "Beautier Profiles"

    auth_user = models.OneToOneField("AuthUser", on_delete=models.DO_NOTHING)
    preferred_name = models.CharField(max_length=64, blank=True)
    specialties = models.ManyToManyField("Specialty")
    calendar_id = models.CharField(max_length=128, null=True)
    availability = JSONField(default=dict)
    bio = models.TextField(max_length=1024, blank=True)
    photo_url = models.URLField(max_length=256, blank=True)
    phone = models.CharField(max_length=16, blank=True)
    title = models.CharField(max_length=64, blank=True)


class Specialty(models.Model):
    class Meta:
        verbose_name_plural = "Specialties"

    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Specialty ID: {self.id} - {self.name}"


class ServiceCategory(models.Model):
    class Meta:
        verbose_name_plural = "Service Categories"

    name = models.CharField(max_length=50)
    panel = models.BooleanField(default=False)
    services = models.ManyToManyField("Service", related_name="category_services")
    active = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Service(models.Model):

    service_id = models.CharField(max_length=20)
    specialties = models.ManyToManyField("Specialty")
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=512)
    extras = models.CharField(max_length=512, blank=True, null=True)
    includes_eyelashes = models.BooleanField(default=False)
    availability = JSONField()
    duration = models.TimeField()
    active = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class WorkOrder(models.Model):
    class Meta:
        verbose_name_plural = "Work Orders"

    request_date = models.CharField(null=True, max_length=10)
    request_time = models.CharField(null=True, max_length=8)
    place_id = models.CharField(max_length=512, null=True, blank=True)
    address = models.JSONField(default=dict)
    customer_profile = models.ForeignKey("CustomerProfile", on_delete=models.DO_NOTHING)
    line_items = models.ManyToManyField("LineItem")
    notes = models.CharField(max_length=256, blank=True)
    status = models.CharField(max_length=32, default="initial_request")
    payment_id = models.CharField(max_length=64, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.__dict__}"


class LineItem(models.Model):
    class Meta:
        verbose_name_plural = "Line Items"

    service = models.ForeignKey("Service", on_delete=models.DO_NOTHING)
    service_date = models.CharField(null=True, max_length=10)
    service_time = models.CharField(null=True, max_length=8)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    staff_assignments = models.ManyToManyField("StaffAssignment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.__dict__}"


class StaffAssignment(models.Model):
    class Meta:
        verbose_name_plural = "Staff Assignments"

        constraints = [
            models.UniqueConstraint(
                fields=["line_item", "index"], name="line_item_index"
            )
        ]

    line_item = models.ForeignKey("LineItem", on_delete=models.CASCADE)
    index = models.IntegerField()
    staff_lines = models.ManyToManyField("StaffLine")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.__dict__}"


class StaffLine(models.Model):
    class Meta:
        verbose_name_plural = "Staff Lines"

    staff_assignment = models.ForeignKey("StaffAssignment", on_delete=models.CASCADE)
    auth_user = models.ForeignKey(
        "AuthUser", null=True, default=None, on_delete=models.DO_NOTHING
    )
    pay_out = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.__dict__}"


class Region(models.Model):
    class Meta:
        verbose_name_plural = "Regions"

        constraints = [
            models.UniqueConstraint(
                fields=["code", "country_code", "state_province_code"],
                name="unique_region",
            )
        ]

    code = models.CharField(max_length=4)
    country_code = models.CharField(max_length=3)
    state_province_code = models.CharField(max_length=3, null=True, blank=True)
    display_name = models.CharField(max_length=32, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code}-{self.state_province_code}-{self.country_code}"


class ServiceRegion(models.Model):
    class Meta:
        abstract = True

    service = models.ForeignKey("Service", on_delete=models.CASCADE)
    region = models.ForeignKey("Region", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ServiceInternalCost(ServiceRegion):
    class Meta:
        verbose_name_plural = "Service Internal Costs"

        constraints = [
            models.UniqueConstraint(
                fields=["service", "region"], name="unique_service_internal_cost"
            )
        ]

    internal_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.__dict__}"


class ServicePayout(ServiceRegion):
    class Meta:
        verbose_name_plural = "Service Payouts"

        constraints = [
            models.UniqueConstraint(
                fields=["service", "region"], name="unique_service_payout"
            )
        ]

    payout = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.__dict__}"


class ServicePublicPrice(ServiceRegion):
    class Meta:
        verbose_name_plural = "Service Public Prices"

        constraints = [
            models.UniqueConstraint(
                fields=["service", "region"], name="unique_service_public_price"
            )
        ]

    public_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.service} {self.region}"
