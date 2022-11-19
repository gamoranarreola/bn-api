from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AuthUserChangeForm, AuthUserCreationForm
from .models import (
    AuthUser,
    BeautierProfile,
    CustomerProfile,
    Region,
    Service,
    ServiceCategory,
    ServiceInternalCost,
    ServicePayout,
    ServicePublicPrice,
)


class AuthUserAdmin(UserAdmin):

    add_form = AuthUserCreationForm
    form = AuthUserChangeForm
    model = AuthUser

    list_display = (
        "id",
        "email",
        "last_name",
        "first_name",
        "is_staff",
        "is_active",
    )

    list_filter = ("email", "last_name", "first_name", "is_staff", "is_active")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    search_fields = ("email",)
    ordering = ("email",)


class CustomerProfileAdmin(admin.ModelAdmin):

    list_display = ("auth_user", "customer_profile_id")

    readonly_fields = (
        "auth_user",
        "customer_profile_id",
    )


class BeautierProfileAdmin(admin.ModelAdmin):

    list_display = (
        "auth_user",
        "calendar_id",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "auth_user",
                    "preferred_name",
                    "title",
                    "specialties",
                    "bio",
                    "photo_url",
                    "phone",
                )
            },
        ),
    )


class RegionAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "state_province_code",
        "country_code",
        "display_name",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "code",
                    "state_province_code",
                    "country_code",
                    "display_name",
                )
            },
        ),
    )


class ServicePublicPriceAdmin(admin.ModelAdmin):

    list_display = (
        "service",
        "region",
        "public_price",
    )

    list_filter = ("region",)

    readonly_fields = (
        "service",
        "region",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "service",
                    "region",
                    "public_price",
                )
            },
        ),
    )


class ServiceInternalCostAdmin(admin.ModelAdmin):

    list_display = (
        "service",
        "region",
        "internal_cost",
    )

    list_filter = ("region",)

    readonly_fields = (
        "service",
        "region",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "service",
                    "region",
                    "internal_cost",
                )
            },
        ),
    )


class ServicePayoutAdmin(admin.ModelAdmin):

    list_display = (
        "service",
        "region",
        "payout",
    )

    list_filter = ("region",)

    readonly_fields = (
        "service",
        "region",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "service",
                    "region",
                    "payout",
                )
            },
        ),
    )


admin.site.register(AuthUser, AuthUserAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin)
admin.site.register(ServiceCategory)
admin.site.register(Service)
admin.site.register(Region, RegionAdmin)
admin.site.register(ServicePublicPrice, ServicePublicPriceAdmin)
admin.site.register(ServiceInternalCost, ServiceInternalCostAdmin)
admin.site.register(ServicePayout, ServicePayoutAdmin)
admin.site.register(BeautierProfile, BeautierProfileAdmin)
