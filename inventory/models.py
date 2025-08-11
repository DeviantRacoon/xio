from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class EquipmentModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.brand} {self.name}"


class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    STATUS_CHOICES = [
        ('new', 'Nuevo'),
        ('used', 'Usado'),
        ('repair', 'En reparación'),
        ('retired', 'Dado de baja'),
    ]

    serial_number = models.CharField(max_length=100, unique=True)
    internal_code = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    model = models.ForeignKey(EquipmentModel, on_delete=models.PROTECT)
    specs = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.internal_code


class InventoryMovement(models.Model):
    MOVEMENT_TYPES = [
        ('purchase', 'Entrada - Compra'),
        ('return', 'Entrada - Devolución'),
        ('assignment', 'Salida - Asignación'),
        ('disposal', 'Salida - Baja'),
        ('maintenance', 'Salida - Mantenimiento'),
    ]

    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='movements')
    type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_type_display()} - {self.equipment}"
