from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from .models import User, UserProfile


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('full_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',),
        }),
    )
    list_display = ('email', 'full_name', 'is_superuser', 'is_staff')
    search_fields = ('email', 'full_name')
    ordering = ('email',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Define UserProfile model for custom User model."""
    readonly_fields = ('updated_date',)

    fieldsets = (
        (None, {'fields': ('email',)}),
        (_('Personal info'), {'fields': ('full_name', 'phone', 'birth_date', 'gender')}),
        (_('Important dates'), {'fields': ('updated_date',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'full_name', 'phone', 'birth_date', 'gender')
    search_fields = ('email', 'full_name')
    ordering = ('email',)


admin.site.unregister(Group)
