from django.db import models

from simple_history.models import HistoricalRecords


from apps.base.models import BaseModel

# Create your models here.


class Beneficiary(BaseModel):
    
    name = models.CharField('Nombre', max_length=100, unique=True)
    interbank_code = models.CharField('Clave interbancaria', max_length=20)
    bank = models.CharField('Banco', max_length=50, null=True)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Beneficiaro'
        verbose_name_plural = 'Beneficiaro'

    def __str__(self):
        return str(self.name)