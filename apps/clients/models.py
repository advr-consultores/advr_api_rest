from django.db import models

from apps.base.models import BaseModel

from simple_history.models import HistoricalRecords

# Create your models here.


class Client(BaseModel):

    name = models.CharField('Nombre', max_length=20, unique=True)
    image = models.ImageField('Imagen', upload_to='static/images/clients/', max_length=255, null=True, blank=True)
    address = models.TextField('Dirección', null=True, blank=True)
    rfc = models.CharField('RFC', max_length=14,unique=True, null=True, blank=True)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return str(self.name)
