from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("price_at_purchase",)

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id", 
        "user", 
        "total_amount", 
        "payment_status",
        "created_at"
    )
    list_filter = ("payment_status", "created_at")
    search_fields = ("user__username", "id")
    readonly_fields = ("created_at",)
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)

# Optional: if you don't want OrderItem to appear separately in admin
# admin.site.unregister(OrderItem)
