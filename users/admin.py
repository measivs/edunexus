from django.contrib import admin
from django.db.models import Model

from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass