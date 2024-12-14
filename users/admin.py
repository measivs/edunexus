from django.contrib import admin
from django.db.models import Model

from .models import CustomUser, AccountBalance


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass

@admin.register(AccountBalance)
class AccountBalanceAdmin(admin.ModelAdmin):
    pass
