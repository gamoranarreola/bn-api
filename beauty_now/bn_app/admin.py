from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from beauty_now.bn_app.models import BeautierProfile, BeautierProfileSpecialty, CustomUser, CustomerProfile
from beauty_now.bn_app.forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = (
        'email',
        'last_name',
        'first_name',
        'is_staff',
        'is_active',
    )

    list_filter = (\
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
                )
            }
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_staff',
                    'is_active',
                )
            }
        ),
    )

    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'password1',
                    'password2',
                    'is_staff',
                    'is_active'
                )
            }
        )
    )

    search_fields = ('email',)
    ordering = ('email',)


class CustomerProfileAdmin(admin.ModelAdmin):

    list_display = (
        'custom_user',
        'customer_profile_id'
    )

    readonly_fields = (
        'custom_user',
        'customer_profile_id',
    )


class BeautierSpecialtyInline(admin.TabularInline):

    model = BeautierProfileSpecialty


class BeautierProfileAdmin(admin.ModelAdmin):

    list_display = (
        'custom_user',
        'calendar_id',
    )

    inlines = [
        BeautierSpecialtyInline,
    ]

    readonly_fields = ('custom_user',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin)
admin.site.register(BeautierProfile, BeautierProfileAdmin)
