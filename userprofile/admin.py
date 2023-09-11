from django.contrib import admin
from .models import Customer, CustomerUser, Staff

class BaseAdmin(admin.ModelAdmin):
    search_fields = ['full_name', 'user']

@admin.register(Customer)
class CustomerAdmin(BaseAdmin):
    list_display = ['user', 'contact', 'district', 'house_number', 'road']  
    search_fields = ['user__username']

@admin.register(CustomerUser)
class CustomerUserAdmin(BaseAdmin):
    list_display = ['user', 'firstname', 'lastname', 'email', 'dob', 'sex']
    search_fields = ['user__username']

    def full_name(self, obj):
        return f"{obj.firstname} {obj.lastname}"

@admin.register(Staff)
class StaffAdmin(BaseAdmin):
    list_display = ['full_name', 'gender', 'dob', 'email', 'contact']
    search_fields = ['firstname', 'lastname']

    def full_name(self, obj):
        return f"{obj.firstname} {obj.lastname}"
    full_name.short_description = 'Full Name'
