from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from simple_history.models import HistoricalRecords

# models
from apps.base.models import BaseModel
from apps.territories.models import Province, Municipality


# Create your models here.
class UserManager(BaseUserManager):
    def _create_user(self, username, email, name, last_name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            name=name,
            last_name=last_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, name, last_name, password=None, **extra_fields):
        return self._create_user(username, email, name, last_name, password, False, False, **extra_fields)

    def create_superuser(self, username, email, name, last_name, password=None, **extra_fields):
        return self._create_user(username, email, name, last_name, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField('Correo Electrónico', max_length=255, unique=True)
    name = models.CharField('Nombres', max_length=255, blank=True, null=True)
    last_name = models.CharField('Apellidos', max_length=255, default="F' M'")
    image = models.ImageField('Imagen de perfil', upload_to='static/images/perfil/', max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    historical = HistoricalRecords()
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    @property
    def fathers_last_name(self):
        return self.last_name[2:self.last_name.find(" M'")] if -1 < self.last_name.find("F'") else ''
    
    @property
    def mothers_last_name(self):
        return self.last_name[self.last_name.find(" M'")+3:] if -1 < self.last_name.find(" M'") else ''

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'last_name']

    def natural_key(self):
        return (self.username)

    def __str__(self):
        return f'{self.name} {self.last_name}'


class Charge(BaseModel):
    
    charge = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, verbose_name='Usuario a cargo', related_name='provinces_charge')
    provinces = models.ManyToManyField(Province, verbose_name='Estados', related_name='users_charge', default=[])

    class Meta:
        verbose_name = 'Usuario a cargo'
        verbose_name_plural = 'Usuarios a cargo'
    
    def __str__(self):
        return str(self.charge.name)
    

class Contact(BaseModel):
    
    name = models.CharField('Nombre', max_length=100)
    last_name = models.CharField('Apellidos', max_length=100)
    phone_one = models.CharField('Número telefónico 1', max_length=15, unique=True)
    phone_two = models.CharField('Número telefónico 2', max_length=15, default='')
    email = models.EmailField('Correo electrónico', max_length=254, unique=True)
    municipalities = models.ManyToManyField(Municipality, verbose_name='Municipios', related_name='users_field', default=[])


    class Meta:
        verbose_name = 'Usuario en campo'
        verbose_name_plural = 'Usuarios en campo'
    
    def __str__(self):
        return str(self.name)
