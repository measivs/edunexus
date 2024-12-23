from django.contrib import admin
from .models import Category, Tag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'parent', 'created_at')
    list_filter = ('parent', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('created_at',)
    prepopulated_fields = {'name': ('description',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    ordering = ('created_at',)
