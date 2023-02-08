from django.db import models

# Create your models here.


class Province(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Estado', max_length=40, unique=True)
    key = models.CharField(max_length=2, null=True, blank=False)
    abbreviation =  models.CharField('Abreviatura', max_length=10, null=True, blank=False, unique=True)
    active = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

    def __str__(self):
        return str(self.name)

class Municipality(models.Model):
    id = models.AutoField(primary_key=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='municipalities')
    key = models.CharField(max_length=3, null=True)
    name = models.CharField('Municipio', max_length=100, unique=False)
    active = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'

    def __str__(self):
        return str(self.name)

class  Locality(models.Model):
    id = models.AutoField(primary_key=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='locality')
    key = models.CharField(max_length=4, null=False)
    name = models.CharField('Localidad', max_length=100)
    carta = models.CharField(max_length=10, blank=True)
    active = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Localidad'
        verbose_name_plural = 'Localidades'

    def __str__(self):
        return str(self.name)
