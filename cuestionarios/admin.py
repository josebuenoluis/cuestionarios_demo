from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([Usuarios,Temas,Preguntas,
                     Respuestas,Estadisticas,Cuestionarios])