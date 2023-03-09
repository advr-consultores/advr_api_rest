from django.contrib import admin

from apps.resources.models import *

# Register your models here.

class PetitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'state', 'work', 'amount', 'bank', 'method_pay', 'bank_data', 'beneficiary', 'resource',)

class ResourceAdmin(admin.ModelAdmin):
    list_display=('id', 'state', 'type_pay', 'pay_separately',  'concept', 'request', 'validate', 'confirm')

admin.site.register(Petition, PetitionAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(UploadFileForm)
admin.site.register(Comment)