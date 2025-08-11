from django.db import migrations


def create_perms(apps, schema_editor):
    Permission = apps.get_model('accounts', 'Permission')
    permissions = [
        ('user_view', 'Ver usuarios'),
        ('user_create', 'Crear usuarios'),
        ('user_edit', 'Editar usuarios'),
        ('user_delete', 'Eliminar usuarios'),
        ('role_view', 'Ver roles'),
        ('role_create', 'Crear roles'),
        ('role_edit', 'Editar roles'),
        ('role_delete', 'Eliminar roles'),
        ('permission_view', 'Ver permisos'),
        ('permission_create', 'Crear permisos'),
        ('permission_edit', 'Editar permisos'),
        ('permission_delete', 'Eliminar permisos'),
    ]
    for code, name in permissions:
        Permission.objects.get_or_create(code=code, defaults={'name': name})


def remove_perms(apps, schema_editor):
    Permission = apps.get_model('accounts', 'Permission')
    codes = [
        'user_view', 'user_create', 'user_edit', 'user_delete',
        'role_view', 'role_create', 'role_edit', 'role_delete',
        'permission_view', 'permission_create', 'permission_edit', 'permission_delete'
    ]
    Permission.objects.filter(code__in=codes).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_perms, reverse_code=remove_perms),
    ]
