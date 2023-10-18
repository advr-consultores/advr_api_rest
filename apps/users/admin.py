from django.contrib import admin
from apps.users.models import User, Charge, Contact

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser', )


class UserCharge(admin.ModelAdmin):
    list_display = ('id', 'charge')


class UserField(admin.ModelAdmin):
    list_display = ('id', 'name', )


admin.site.register(User, UserAdmin)
admin.site.register(Charge, UserCharge)
admin.site.register(Contact, UserField)
