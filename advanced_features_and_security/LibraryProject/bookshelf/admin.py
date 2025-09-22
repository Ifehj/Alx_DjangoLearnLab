from django.contrib import admin
from .models import Book, CustomUser
from django.contrib.auth.admin import UserAdmin


admin.site.register(Book, CustomUser)
class BookAdmin(admin.ModelAdmin):
    # columns to show in the list view
    list_display = ('title', 'author', 'publication_year')

    # enable right-side filter box (by year and author)
    list_filter = ('publication_year', 'author')

    # enable search box (search by title and author)
    search_fields = ('title', 'author')

    # clickable column 
    list_display_links = ('title',)

    # default ordering
    ordering = ('title',)

    # pagination
    list_per_page = 25

class CustomUserAdmin(UserAdmin):
    """Admin configuration for CustomUser"""

    model = CustomUser
    list_display = ("username", "email", "date_of_birth", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "date_of_birth")

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("date_of_birth", "profile_photo")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "date_of_birth", "profile_photo", "password1", "password2", "is_staff", "is_active")}
        ),
    )

    search_fields = ("username", "email")
    ordering = ("username",)