from django.contrib import admin
from .models import Vehicle, Upgrade

# Register your models here.

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "base_hp", "base_torque")

@admin.register(Upgrade)
class UpgradeAdmin(admin.ModelAdmin):
    list_display = ("id", "vehicle", "part", "hp_gain", "torque_gain")
