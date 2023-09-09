from django.contrib import admin
from django.utils.html import format_html
from .models import Size, AddProduct, OrderDetail, ProductSize  # Import ProductSize, not ProductImage

admin.site.register(Size)
admin.site.register(OrderDetail)

class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'formatted_price')
    list_filter = ('product', 'size')
    search_fields = ('product__product_name', 'size__size_name')

    def formatted_price(self, obj):
        return f"${obj.price:.2f}"

    formatted_price.short_description = 'Price'

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('display_image', 'product_name', 'image_name', 'product_category')
    list_filter = ('product__category',)
    search_fields = ('product__product_name',)

    def display_image(self, obj):
        return self.get_image_tag(obj.image)

    def get_image_tag(self, image):
        return format_html('<img src="{}" style="max-width: 100px; max-height: 100px; border-radius: 5px;"/>', image.url)

    display_image.allow_tags = True
    display_image.short_description = 'Image'

    def product_name(self, obj):
        return obj.product.product_name

    def image_name(self, obj):
        return obj.image.name

    def product_category(self, obj):
        return obj.product.get_category_display()

    product_name.short_description = 'Product Name'
    image_name.short_description = 'Image Name'
    product_category.short_description = 'Product Category'

class ProductImageInline(admin.TabularInline):
    model = ProductSize  # Use ProductImage for the inline

class AddProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'display_sizes', 'display_price', 'display_image')
    list_filter = ('category',)
    search_fields = ('product_name', 'category__name')
    
    inlines = [ProductImageInline]  # Add the inline for ProductImage

    def display_sizes(self, obj):
        return ', '.join([size.size.get_size_display() for size in obj.sizes.all()])

    def display_price(self, obj):
        return f"${obj.sizes.first().price:.2f}" if obj.sizes.exists() else "N/A"

    def display_image(self, obj):
        # Retrieve the first image associated with the product
        product_sizes = obj.sizes.all()
        if product_sizes:
            first_product_size = product_sizes[0]
            if first_product_size.images:
                first_image = first_product_size.images.url
                return format_html(
                    '<img src="{}" style="border-radius: 5px; width: 100px; height: 100px; object-fit: cover;" />',
                    first_image
                )
        return "No Image"

    display_image.allow_tags = True
    display_image.short_description = 'Image'

    display_sizes.short_description = 'Sizes'

admin.site.register(AddProduct, AddProductAdmin)
admin.site.register(ProductSize, ProductPriceAdmin)  # Register ProductSize with ProductPriceAdmin
