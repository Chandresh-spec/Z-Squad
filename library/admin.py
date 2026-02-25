from django.contrib import admin
from .models import UserFile, UserReadingData


@admin.register(UserFile)
class UserFileAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "file_type", "size", "uploaded_at"]
    list_filter = ["file_type", "uploaded_at"]
    search_fields = ["title", "user__email"]
    readonly_fields = ["uploaded_at", "size"]


@admin.register(UserReadingData)
class UserReadingDataAdmin(admin.ModelAdmin):
    list_display = ["user", "file", "progress", "bookmarked", "updated_at"]
    list_filter = ["bookmarked"]
    search_fields = ["user__email", "file__title"]
