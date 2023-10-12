from django.contrib import admin

from apps.resources.models import *

# Register your models here.

# class PetitionAdmin(admin.ModelAdmin):
#     list_display = ('id', 'state', 'work', 'amount')

# class ResourceAdmin(admin.ModelAdmin):
#     list_display=('id', 'state')

admin.site.register(Petition)
admin.site.register(Resource)
admin.site.register(UploadFileForm)
admin.site.register(Comment)