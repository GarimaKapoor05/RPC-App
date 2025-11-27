from django.contrib import admin
from .models import Pen, Refill

@admin.register(Pen)
class PenAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_vintage', 'quantity', 'on_sale', 'in_stock')
    search_fields = ('name', 'category')
    list_filter = ('category', 'is_vintage', 'on_sale', 'in_stock')

@admin.register(Refill)
class RefillAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'size', 'ink_color', 'price', 'quantity', 'in_stock')
    search_fields = ('name', 'brand', 'category', 'ink_color')
    list_filter = ('category', 'ink_color', 'brand', 'in_stock')
