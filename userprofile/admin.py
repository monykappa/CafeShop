from django.contrib import admin
from .models import Customer, CustomerUser, Staff

class BaseAdmin(admin.ModelAdmin):
    search_fields = ['full_name','user']

@admin.register(Customer)
class CustomerAdmin(BaseAdmin):
    list_display = ['user', 'contact', 'location']
    

@admin.register(CustomerUser)
class CustomerUserAdmin(BaseAdmin):
    list_display = ['user', 'firstname', 'lastname', 'email', 'dob', 'sex']

    def full_name(self, obj):
        return f"{obj.firstname} {obj.lastname}"

@admin.register(Staff)
class StaffAdmin(BaseAdmin):
    list_display = ['full_name', 'gender', 'dob', 'email', 'contact']
    search_fields = ['firstname', 'lastname']

    def full_name(self, obj):
        return f"{obj.firstname} {obj.lastname}"
    full_name.short_description = 'Full Name'
