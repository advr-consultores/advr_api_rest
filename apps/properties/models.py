from django.db import models

from simple_history.models import HistoricalRecords

# models
from apps.base.models import BaseModel
from apps.territories.models import Province, Municipality, Locality
from apps.clients.models import Client

# Create your models here.

class Property(BaseModel):

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente', related_name='inmubles')
    name = models.CharField('Nombre', max_length=50)
    property_key = models.CharField('Clave', max_length=10, unique=True)
    sirh = models.CharField('Convenio o SIRH', max_length=10, null=True, blank=True)
    address = models.TextField('Dirección', null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name='Estado')
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, verbose_name='Municipio')
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Localidad')
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Inmueble'
        verbose_name_plural = 'Inmuebles'
    
    def __str__(self):
        return str(self.name)
