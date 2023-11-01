from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino')
    )

    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField()
    nombres = models.CharField(max_length=30, blank=True)
    apellidos = models.CharField(max_length=30, blank=True)
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    codregistro = models.CharField(max_length=6, blank=True)


    #PARAMETROS PARA INGRESAR AL ADMIN DE DJANGO
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = UserManager()

    #ESTABLECER CAMPO DE INICIO DE SESION
    USERNAME_FIELD = 'username'

    #ESPECIFICAMOS CAMPOS REQUERIDOS
    REQUIRED_FIELDS = ['nombres', 'email']

    class Meta:

        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.nombres + ' ' + self.apellidos