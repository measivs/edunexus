from django.contrib import admin
from orders.models import Order, Coupon

# @admin.action(description='Mark selected orders as Completed')
# def mark_as_completed(modeladmin, request, queryset):
#     for order in queryset:
#         if order.status == 'created':
#             order.mark_completed()
#
#
# @admin.action(description='Mark selected orders as Cancelled')
# def mark_as_cancelled(modeladmin, request, queryset):
#     for order in queryset:
#         if order.status == 'created':
#             order.mark_cancelled()

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'amount', 'status', 'created_at')


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    pass
