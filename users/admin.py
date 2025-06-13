from django.contrib import admin

from users.models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'email_verified')
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')