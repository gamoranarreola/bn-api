from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import AuthUser, CustomerProfile
from .forms import AuthUserCreationForm, AuthUserChangeForm


class AuthUserAdmin(UserAdmin):

    add_form = AuthUserCreationForm
    form = AuthUserChangeForm
    model = AuthUser

    list_display = (
        'id',
        'email',
        'last_name',
        'first_name',
        'is_staff',
        'is_active',
    )

    list_filter = (
        'email',
        'last_name',
        'first_name',
        'is_staff',
        'is_active'
    )

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'password',
                ),
            },
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_staff',
                    'is_active',
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': (
                    'wide',
                ),
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'password1',
                    'password2',
                    'is_staff',
                    'is_active',
                ),
            },
        ),
    )

    search_fields = ('email',)
    ordering = ('email',)


class CustomerProfileAdmin(admin.ModelAdmin):

    list_display = (
        'auth_user',
        'customer_profile_id'
    )

    readonly_fields = (
        'auth_user',
        'customer_profile_id',
    )


"""
class BeautierSpecialtyInline(admin.TabularInline):

    model = BeautierProfileSpecialty


class BeautierProfileAdmin(admin.ModelAdmin):

    list_display = (
        'auth_user',
        'calendar_id',
    )

    inlines = [
        BeautierSpecialtyInline,
    ]

    readonly_fields = ('auth_user',)

admin.site.register(AuthUser, AuthUserAdmin)
admin.site.register(BeautierProfile, BeautierProfileAdmin)
"""
admin.site.register(AuthUser, AuthUserAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin)
