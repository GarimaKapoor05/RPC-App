from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'full_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'full_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'full_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)
