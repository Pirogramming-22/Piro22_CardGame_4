from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = (
        (None, {'fields': ('id', 'password')}),
        ('Personal info', {'fields': ('nickname', 'score', 'login_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id', 'nickname', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )
    list_display = ('id', 'nickname', 'score', 'is_active', 'is_staff', 'login_type')
    search_fields = ('id', 'nickname')
    ordering = ('id',)