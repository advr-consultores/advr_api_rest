from django.contrib import admin

from apps.properties.models import Property
# Register your models here.

class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'property_key', 'client', 'province', 'municipality')

admin.site.register(Property, BranchAdmin)
