from django.contrib import admin
from apps.territories.models import Province, Municipality, Locality

# Register your models here.

class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'abbreviation', 'key', 'active')

class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'province', 'key', 'active')

class LocalityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'municipality', 'key', 'active')

admin.site.register(Province, ProvinceAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(Locality, LocalityAdmin)
