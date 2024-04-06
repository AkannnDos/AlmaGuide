from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from users.models import User

try:
    admin.site.unregister(Group)
except Exception:
    pass


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'email', 'full_name', 'phone_number', 'is_active',
    )
    list_display_links = (
        'email', 'full_name', 'phone_number', 'is_active',
    )

    readonly_fields = ('date_joined', 'last_login')
    fieldsets = (
        (_('Main info'), {'fields': (
            'email', 'password', 'full_name', 'phone_number', 'photo',
            'is_active', 'is_staff', 'is_superuser',
        )}),
        (_('Important dates'), {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        (_('Main info'), {'fields': (
            'email', 'password', 'full_name', 'phone_number', 'photo',
            'is_active', 'is_staff', 'is_superuser',
            'password1', 'password2',
        )}),
    )
    list_filter = ('is_superuser', 'is_staff', 'is_active')

    search_fields = ('full_name', 'phone_number', 'email')
    ordering = ('-id',)
    filter_horizontal = ()
    change_password_form = AdminPasswordChangeForm
