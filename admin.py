from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import Balance, User

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email', 'phone', 'email_or_phone')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('username', 'email_or_phone', 'is_staff')
    search_fields = ('username', 'email', 'phone', 'email_or_phone')


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):

    list_display = ('user', 'balance')
    list_display_links = ('user', )
    list_filter = ('user', )
    readonly_fields = ('modified', 'created')

    search_fields = ['user']
