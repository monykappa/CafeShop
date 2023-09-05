from django.contrib import admin
from django.utils.html import format_html
from .models import Size, AddProduct, OrderDetail

admin.site.register(Size)
admin.site.register(OrderDetail)

class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'formatted_price')
    list_filter = ('product', 'size')
    search_fields = ('product__product_name', 'size__size_name')  # Add the fields you want to search

    def formatted_price(self, obj):
        return f"${obj.price:.2f}"

    formatted_price.short_description = 'Price'

class AddProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'display_image', 'category', 'display_sizes', 'price')
    list_filter = ('category',)
    search_fields = ('product_name', 'category__name')
    
    def display_image(self, obj):
        return format_html('<img src="{}" width="80px" height="70px" style="border-radius: 5px;" />', obj.image.url)

    def display_sizes(self, obj):
        return ', '.join([size.size for size in obj.sizes.all()])



    display_image.allow_tags = True
    display_image.short_description = 'Image'
    display_sizes.short_description = 'Sizes'

admin.site.register(AddProduct, AddProductAdmin)
