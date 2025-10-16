from django.db import models
from django.contrib.auth.models import AbstractUser
from panel.utils import obtener_avatares_cache
import uuid
# Create your models here.

avatares = obtener_avatares_cache()

class Usuarios(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.TextField(blank=True,default=avatares[0]) 

    class Meta:
        db_table = 'Usuarios'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

class TypeChoices(models.TextChoices):
    EMAIL = 'email', 'email'
    PASSWORD = 'password', 'password'

class TokenChange(models.Model):
    user_fk = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    type = models.CharField(max_length=50, choices=TypeChoices.choices, default=TypeChoices.EMAIL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Token for {self.user_fk.username}: {self.token}'

    class Meta:
        db_table = 'TokenChange'
        verbose_name = "Token de Cambio"
        verbose_name_plural = "Tokens de Cambio"