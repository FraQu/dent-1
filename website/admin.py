from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from .models import User, Customer, Employee


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_customer', 'is_employee',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',),
        }),
    )
    list_display = ('email', 'is_superuser', 'is_staff', 'is_customer', 'is_employee')
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Define UserProfile model for custom User model."""
    readonly_fields = ('updated_date',)

    fieldsets = (
        (None, {'fields': ('email',)}),
        (_('Personal info'), {'fields': ('full_name', 'phone', 'birth_date', 'gender',)}),
        (_('Important dates'), {'fields': ('updated_date',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', )
    search_fields = ('email', )
    ordering = ('email',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Define StaffProfile model for custom User model."""
    readonly_fields = ('updated_date',)

    fieldsets = (
        (None, {'fields': ('email',)}),
        (_('Personal info'), {'fields': ('full_name', 'bio',)}),
        (_('Important dates'), {'fields': ('updated_date',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'full_name',)
    search_fields = ('email',)
    ordering = ('email',)


admin.site.unregister(Group)
