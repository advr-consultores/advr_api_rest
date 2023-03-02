from django.contrib import admin

from apps.projects.models import Project, Concept

# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )

class ConceptAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'name')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Concept, ConceptAdmin)
