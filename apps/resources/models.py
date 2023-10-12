from django.db import models

from simple_history.models import HistoricalRecords

from apps.base.models import BaseModel
from apps.works.models import Work
from apps.users.models import User
from apps.beneficiary.models import Beneficiary

# Create your models here.


class Petition(BaseModel):
    
    work = models.OneToOneField(Work, on_delete=models.CASCADE, verbose_name='Trabajo', related_name='petition')
    amount = models.FloatField('Importe')
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Petición'
        verbose_name_plural = 'Peticiones'

    def __str__(self):
        return str(self.work.concept)


class Resource(BaseModel):

    PAYMENT_MODE = [
        ('transferencia', 'Transferencia'),
        ('cheque', 'Cheque')
    ]

    TRANSFER_TYPE = [
        ('transferencia', 'Transferencia'),
        ('cuenta', 'Cuenta'),
        ('servicio', 'Servicio')
    ]

    petitions = models.ManyToManyField(Petition, verbose_name='Trabajos', related_name='resource')
    payment_mode = models.CharField('Modalidad pago', max_length=30, choices=PAYMENT_MODE, blank=True)
    transfer_type = models.CharField('Tipo transferencia', max_length=30, choices=TRANSFER_TYPE, blank=True)
    transfer_data = models.TextField('Comentario', default='{}')
    bank = models.CharField('Banco', max_length=50, null=True)
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, verbose_name='Beneficiario', null=True)
    concept = models.TextField('Concepto de pago')
    validate = models.BooleanField('Validado', default=False)
    paid = models.BooleanField('Pagado', default=False)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @property
    def total_amout(self):
        qs = self.petitions.through.objects.filter(resource=self.id).aggregate(total_amount=models.Sum('petition__amount'))
        return "$%0.2f" % qs['total_amount']

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'

    def __str__(self):
        return str(self.id)


class UploadFileForm(BaseModel):

    file = models.FileField(upload_to='static/archivos/recursos')
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='upload_by', verbose_name='Usuario')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='receipt', verbose_name='Comprobante de pago')
    historial = HistoricalRecords()

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Comprobante'
        verbose_name_plural = 'Comprobantes'


class Comment(BaseModel):

    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='comment', verbose_name='Solicitud de recursos')
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Usuario')
    comment = models.TextField('Comentario', default='Algún comentario')
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
        return str(self.changed_by.username)
