"""
Django Admin for Model registering
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    """ Define admin pages for users """
    ordering = ['id']
    list_display = ['email', 'name']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_support')}),
        (_('Important Dates'), {'fields': ('last_login',)})
    )
    readonly_fields = ['last_login']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
                'is_support',
            )
        }
        ),
    )


admin.site.register(models.User, UserAdmin)
