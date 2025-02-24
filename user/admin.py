from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (  # Extend default fields
        ('Additional Info', {'fields': ('phone_number', 'address')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
