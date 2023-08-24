from django.contrib import admin
from .models import Size, Product, ProductPrice, OrderDetail

admin.site.register(Size)
admin.site.register(Product)
admin.site.register(OrderDetail)

class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'formatted_price')  # Include 'formatted_price' for display
    list_filter = ('product', 'size')
    search_fields = ('product__product_name', 'size__size_name')

    # Define a custom method to format the price
    def formatted_price(self, obj):
        return f"${obj.price:.2f}"

    formatted_price.short_description = 'Price'  # Set the column header in the admin

admin.site.register(ProductPrice, ProductPriceAdmin)
