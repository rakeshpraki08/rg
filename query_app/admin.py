from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomAdminCreationForm, CustomAdminChangeForm
from .models import CustomUser, Regions, Reports, Reports_Data


class CustomUserAdmin(UserAdmin):
    add_form = CustomAdminCreationForm
    form = CustomAdminChangeForm
    model = CustomUser
    list_display = ('email','is_active', 'is_staff', 'is_superuser')
    list_filter = ('email', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'regions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'regions')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Regions)

admin.site.register(Reports)

admin.site.register(Reports_Data)