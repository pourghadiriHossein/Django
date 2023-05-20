from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'status' )}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone', 'status' )}),
    )

    list_display = ['username', 'email', 'phone', 'status' , 'is_staff']
    list_display_links = ['username', 'email', 'phone', 'status' , 'is_staff']


admin.site.register(CustomUser, CustomUserAdmin)