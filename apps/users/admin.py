from django.contrib import admin
from apps.users.models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser', )


admin.site.register(User, UserAdmin)
