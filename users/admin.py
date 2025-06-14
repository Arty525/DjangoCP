from django.contrib import admin

from users.models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_superuser', 'is_banned')
    list_filter = ('username', 'email', 'is_active', 'is_superuser', 'is_banned')
    search_fields = ('username', 'email')