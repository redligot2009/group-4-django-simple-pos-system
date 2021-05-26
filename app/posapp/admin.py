from django.contrib import admin

from .models import Order, Item, OrderItem

# Register your models here.

# admin.site.register(Order)
admin.site.register(Item)
admin.site.register(OrderItem)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields=(
        'payment_type',
        'total_amount_paid')