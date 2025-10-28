from django.contrib import admin
from .models import Device

# Register your models here.

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("name","mac","is_on","desired_state","last_seen","is_online")
    readonly_fields = ("api_key","last_seen","is_online")
    search_fields = ("name","mac","api_key")
