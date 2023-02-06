from django.contrib import admin
from apps.clients.models import Client

# Register your models here.


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rfc', 'address')


admin.site.register(Client, ClientAdmin)
