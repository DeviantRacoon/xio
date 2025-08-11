from django.contrib import admin
from .models import (
    Category,
    Brand,
    EquipmentModel,
    Location,
    Supplier,
    Equipment,
    InventoryMovement,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(EquipmentModel)
class EquipmentModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand')
    list_filter = ('brand',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        'internal_code',
        'serial_number',
        'category',
        'brand',
        'model',
        'status',
        'location',
    )
    list_filter = ('category', 'brand', 'status', 'location')
    search_fields = ('internal_code', 'serial_number')


@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'type', 'date', 'responsible')
    list_filter = ('type', 'date')
