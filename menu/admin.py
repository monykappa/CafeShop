from django.contrib import admin
from .models import Size, AddProduct, OrderDetail

admin.site.register(Size)
admin.site.register(AddProduct)
admin.site.register(OrderDetail)

class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'formatted_price')
    list_filter = ('product', 'size')
    search_fields = ('product__product_name', 'size__size_name')  # Add the fields you want to search

    def formatted_price(self, obj):
        return f"${obj.price:.2f}"

    formatted_price.short_description = 'Price'

