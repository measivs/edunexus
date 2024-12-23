from django.contrib import admin
from orders.models import Order, Coupon

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'course__title', 'status')
    ordering = ('created_at',)
    list_editable = ('status',)

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'discount_percentage', 'valid_until', 'is_active', 'creator', 'created_at')
    list_filter = ('is_active', 'valid_until', 'created_at')
    search_fields = ('code', 'creator__username')
    ordering = ('created_at',)
    list_editable = ('is_active',)
