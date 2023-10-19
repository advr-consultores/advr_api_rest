from django.contrib import admin

from apps.works.models import Work, UploadFileForm, Status, Comment

# Register your models here.

class WorckAdmin(admin.ModelAdmin):
    list_display = ('id', 'concept', 'property_office')

class UploadFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'work')

class WorkStateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'work', 'comment')

admin.site.register(Work, WorckAdmin)
admin.site.register(UploadFileForm, UploadFileAdmin)
admin.site.register(Status, WorkStateAdmin)
admin.site.register(Comment, CommentAdmin)
