from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

class Database(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class User(AbstractBaseUser,PermissionsMixin):
    GENDER_CHOISES = (
        ('M','Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otros'),
    )
    username = models.CharField(max_length=10,unique=True,verbose_name='Usuario')
    email = models.EmailField(verbose_name='e-mail')
    nombres = models.CharField(max_length=50,verbose_name='Nombres')
    apellidos = models.CharField(max_length=50,verbose_name='Apellidos')
    genero = models.CharField(max_length=1,choices=GENDER_CHOISES, blank=True,verbose_name='Género')
    codregistro = models.CharField(max_length=6, blank=True,verbose_name='Código de Registro')
    databases = models.ManyToManyField(Database, blank=True,verbose_name='Bases de datos')
    #
    is_staff = models.BooleanField(default=False,verbose_name='Administrador')
    is_active= models.BooleanField(default=False,verbose_name='Activo')
    is_superuser = models.BooleanField(default=False,verbose_name='Superusuario')
    
    USERNAME_FIELD = 'username'
    
    REQUIRED_FIELDS = ['email']
    
    objects = UserManager()

    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.nombres+' '+self.apellidos
    
    def __str__(self):
        return self.username + ' - ' + self.nombres + ' - ' +self.apellidos+ ' - ' +self.email

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    databases = models.ManyToManyField(Database)