from django.contrib.auth.models import AbstractUser
from django.db import models


class Permission(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:  # pragma: no cover - simple string representation
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(Permission, blank=True, related_name="roles")

    def __str__(self) -> str:  # pragma: no cover - simple string representation
        return self.name


class User(AbstractUser):
    roles = models.ManyToManyField(Role, blank=True, related_name="users")

    def has_perm(self, perm, obj=None):  # pragma: no cover - simple permission check
        if self.is_superuser:
            return True
        return self.roles.filter(permissions__code=perm).exists()

    def has_perms(self, perm_list, obj=None):  # pragma: no cover
        return all(self.has_perm(p, obj) for p in perm_list)
