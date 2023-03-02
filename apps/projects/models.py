from django.db import models

from simple_history.models import HistoricalRecords

# models
from apps.base.models import BaseModel


# Create your models here.
class Project(BaseModel):

    name = models.CharField('Proyecto', max_length=50, unique=True)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'

    def __str__(self):
        return str(self.name)


class Concept(BaseModel):

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='concepts', verbose_name='Proyecto')
    name = models.CharField('Concepto', max_length=50, unique=True)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Concepto'
        verbose_name_plural = 'Conceptos'

    def __str__(self):
        return str(self.name)
