from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin  
from django.contrib.auth.models import User
from .models import Size, AddProduct, OrderDetail, ProductSize, Checkout

admin.site.register(Size)
admin.site.register(Checkout)

class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('checkout_id', 'customer', 'user', 'calculate_total_price')

    def calculate_total_price(self, obj):
        return obj.calculate_total_price()

    calculate_total_price.short_description = 'Total Price'

class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'user_name', 'quantity', 'formatted_total_price')
    list_filter = ('product_size__product', 'user')  # Add any additional filters if needed

    def product_name(self, obj):
        return obj.product_size.product.product_name

    def user_name(self, obj):
        if obj.user:
            return obj.user.username  # Display the username if the user exists
        return "N/A"  # Display "N/A" if there is no user

    def formatted_total_price(self, obj):
        return f"${obj.total_price:.2f}"

    product_name.short_description = 'Product Name'
    user_name.short_description = 'User Name'
    formatted_total_price.short_description = 'Total Price'



admin.site.register(OrderDetail, OrderDetailAdmin)


class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'formatted_price')
    list_filter = ('product', 'size')
    search_fields = ('product__product_name', 'size__size_name')

    def formatted_price(self, obj):
        return f"${obj.price:.2f}"

    formatted_price.short_description = 'Price'


admin.site.register(ProductSize, ProductPriceAdmin)


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
    model = ProductSize





class AddProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'display_price', 'display_image')
    list_filter = ('category',)
    search_fields = ('product_name', 'category__name')

    inlines = [ProductImageInline]

    def display_price(self, obj):
        sizes_and_prices = [f"{size.size.get_size_display()}: ${size.price:.2f}" for size in obj.sizes.all()]
        return ', '.join(sizes_and_prices) if sizes_and_prices else "N/A"

    def display_image(self, obj):
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


admin.site.register(AddProduct, AddProductAdmin)