from django.contrib import admin

from ..models import CustomerProfile, CustomUser


class CustomerProfileAdmin(admin.ModelAdmin):
    """
    BeautierProfile admin.
        
    Arguments:
        ModelAdmin {class} -- ModelAdmin class.
    """

    list_display = (
        'custom_user',
        'customer_profile_id'
    )

    readonly_fields = (
        'custom_user',
        'customer_profile_id',
    )

admin.site.register(CustomerProfile, CustomerProfileAdmin)
