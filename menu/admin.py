from django.contrib import admin
from .models import Size, AddProduct, OrderDetail, Image

class SizeInline(admin.TabularInline):
    model = AddProduct.sizes.through
    extra = 1

class ImageInline(admin.TabularInline):
    model = AddProduct.images.through
    extra = 1

class AddProductAdmin(admin.ModelAdmin):
    inlines = [SizeInline, ImageInline]
    list_display = ('product_name', 'get_sizes', 'formatted_price')
    list_filter = ('category',)
    search_fields = ('product_name', 'sizes__size', 'images__image')

    def get_sizes(self, obj):
        return ", ".join(str(size) for size in obj.sizes.all())

    def get_images(self, obj):
        return ", ".join(str(image) for image in obj.images.all())

    def formatted_price(self, obj):
        return f"${obj.price:.2f}"

    get_sizes.short_description = 'Sizes'
    get_images.short_description = 'Images'
    formatted_price.short_description = 'Price'

admin.site.register(Size)
admin.site.register(Image)
admin.site.register(AddProduct, AddProductAdmin)
admin.site.register(OrderDetail)

