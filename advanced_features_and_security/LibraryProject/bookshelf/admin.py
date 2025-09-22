from django.contrib import admin
from .models import Book, CustomUser


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