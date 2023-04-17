from django.contrib import admin
from orders.models import Order, OrderProduct, Payment

# Register your models here.

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('Payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'tax', 'status', 'ip', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInline]

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'user', 'payment_method', 'amount_paid', 'status']

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['order', 'user', 'product', 'quantity', 'product_price']


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
