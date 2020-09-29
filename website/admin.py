from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from .models import User, Customer, Employee


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define Admin model for custom User model with no username field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('full_name', 'birth_date', 'gender', 'phone', 'profile_pic',)}),
        (_('Permissions'),
         {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_customer', 'is_employee', 'is_nurse', 'is_doctor',
                     'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'is_active', 'full_name', 'birth_date', 'gender', 'phone', 'is_superuser', 'is_staff', 'is_customer', 'is_employee', 'is_nurse', 'is_doctor',)
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Define Customer Admin model for custom User model."""

    readonly_fields = ('updated_date',)

    fieldsets = (
        (None, {'fields': ('email',)}),
        (_('Personal info'), {'fields': ()}),
        (_('Important dates'), {'fields': ('updated_date',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', )
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Define Employee Admin model for custom User model."""

    readonly_fields = ('updated_date',)

    fieldsets = (
        (None, {'fields': ('email',)}),
        (_('Personal info'), {'fields': ('bio',)}),
        (_('Important dates'), {'fields': ('updated_date',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email',)
    search_fields = ('email',)
    ordering = ('email',)


admin.site.unregister(Group)
