from django.db import models

from simple_history.models import HistoricalRecords

from apps.base.models import BaseModel
from apps.works.models import Work
from apps.users.models import User

# Create your models here.


class Petition(BaseModel):
    
    work = models.OneToOneField(Work, on_delete=models.CASCADE, verbose_name='Trabajo', related_name='petition')
    amount = models.FloatField('Importe')
    bank = models.CharField('Banco', max_length=50)
    method_pay = models.CharField('Metodo de pago', max_length=50)
    bank_data = models.CharField('Datos bancarios', max_length=25)
    beneficiary = models.CharField('Beneficiario', max_length=50)
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

    petitions = models.ManyToManyField(Petition, verbose_name='Trabajos', related_name='resource')
    type_pay = models.CharField('Tipo de pago', max_length=30)
    pay_separately = models.BooleanField('Pagar por separado', default=False)
    concept = models.TextField('Concepto de pago')
    request = models.BooleanField('Solicitud', default=False)
    validate = models.BooleanField('Validado', default=False)
    confirm = models.BooleanField('Solicitud confirmada', default=False)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @property
    def total_amout(self):
        qs = self.petitions.through.objects.filter(resource=self.id).aggregate(total_amount=models.Sum('petition__amount'))
        return "$ %0.2f" % qs['total_amount']

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
