from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
	model = CustomUser
	list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
	list_filter = ('is_staff', 'is_active')
	ordering = ('email',)
	search_fields = ('email',)
	fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
