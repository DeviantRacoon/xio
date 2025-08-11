from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Role, Permission


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + ((None, {'fields': ('roles',)}),)
    filter_horizontal = ('roles',)


admin.site.register(Role)
admin.site.register(Permission)
