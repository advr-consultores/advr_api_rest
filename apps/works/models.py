from django.db import models

from simple_history.models import HistoricalRecords

# models
from apps.base.models import BaseModel
from apps.projects.models import Concept
from apps.users.models import User
from apps.properties.models import Property


class Status(BaseModel):

    name = models.CharField('Estado del trabajo', max_length=50, unique=True)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Estado de trabajo'
        verbose_name_plural = 'Estados de los trabajos'

    def __str__(self):
        return self.name


class Work(BaseModel):
    
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE, verbose_name='Concepto')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Estado del trabajo')
    property_office = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='works', verbose_name='Inmuebles')
    assigned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='works', verbose_name='Usuario asignado')
    area_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments', verbose_name='Usuario en campo')
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Trabajo'
        verbose_name_plural = 'Trabajos'

    def __str__(self):
        return self.concept.name

class UploadFileForm(BaseModel):

    name = models.CharField('Nombre del archivo', max_length=50)
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='files', verbose_name='Trabajo')
    file = models.FileField(upload_to='static/archivos/trabajos')
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Archivo'
        verbose_name_plural = 'Archivos'

    def __str__(self):
        return self.title
    
class Comment(BaseModel):
    
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='comments', verbose_name='Comentario')
    comment = models.TextField('Comentario')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')

    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return self.comment