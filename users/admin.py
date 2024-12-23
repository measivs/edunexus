from django.contrib import admin
from .models import CustomUser, AccountBalance

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'is_verified', 'date_joined')
    list_filter = ('role', 'is_verified', 'date_joined')
    search_fields = ('username', 'email', 'role')
    ordering = ('date_joined',)
    list_editable = ('role', 'is_verified')

@admin.register(AccountBalance)
class AccountBalanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'balance')
    search_fields = ('user__username',)
    ordering = ('balance',)
