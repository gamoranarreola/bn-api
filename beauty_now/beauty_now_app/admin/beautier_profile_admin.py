from django.contrib import admin

from ..models import BeautierProfile, BeautierProfileSpecialty


class BeautierSpecialtyInline(admin.TabularInline):
    model = BeautierProfileSpecialty


class BeautierProfileAdmin(admin.ModelAdmin):
    """
    BeautierProfile admin.
        
    Arguments:
        ModelAdmin {class} -- ModelAdmin class.
    """

    list_display = (
        'custom_user',
        'calendar_id',
    )

    inlines = [
        BeautierSpecialtyInline,
    ]

    readonly_fields = ('custom_user',)

admin.site.register(BeautierProfile, BeautierProfileAdmin)
