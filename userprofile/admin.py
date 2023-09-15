from django.contrib import admin
from .models import Customer, CustomerUser, Staff
from django.utils.html import format_html

class BaseAdmin(admin.ModelAdmin):
    search_fields = ['full_name', 'user']

@admin.register(Customer)
class CustomerAdmin(BaseAdmin):
    list_display = ['user', 'contact', 'district', 'house_number', 'road']  
    search_fields = ['user__username']

@admin.register(CustomerUser)
class CustomerUserAdmin(BaseAdmin):
    list_display = ['user', 'firstname', 'lastname', 'email', 'dob', 'sex', 'display_profile_image']  
    search_fields = ['user__username']

    def full_name(self, obj):
        return f"{obj.firstname} {obj.lastname}"

    def display_profile_image(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.profile_image.url)
        else:
            return "No Image"

    display_profile_image.allow_tags = True
    display_profile_image.short_description = 'Profile Image'


@admin.register(Staff)
class StaffAdmin(BaseAdmin):
    list_display = ['full_name', 'gender', 'dob', 'email', 'contact']
    search_fields = ['firstname', 'lastname']

    def full_name(self, obj):
        return f"{obj.firstname} {obj.lastname}"
    full_name.short_description = 'Full Name'
