from django.db import models
from authentication.models import Usuarios
# Create your models here.
class Temas(models.Model):
    nombre = models.CharField(max_length=100,unique=True)

class Cuestionarios(models.Model):
    nombre_cuestionario = models.CharField(max_length=200,null=True,unique=True)
    descripcion_cuestionario = models.TextField(null=True)
    id_tema_fk = models.ForeignKey(Temas,on_delete=models.CASCADE)
    # id_asignatura_fk = models.ForeignKey(Asignaturas,on_delete=models.CASCADE,null=True)
    nombre_usuario_fk = models.ForeignKey(Usuarios,on_delete=models.CASCADE,null=True)
    fecha_creacion = models.DateField(auto_now=True)

class Preguntas(models.Model):
    pregunta = models.TextField(null=False)
    id_cuestionario_fk = models.ForeignKey(Cuestionarios,on_delete=models.CASCADE)

class Respuestas(models.Model):
    respuesta = models.TextField(null=False)
    correcta = models.BooleanField(null=False)
    id_pregunta_fk = models.ForeignKey(Preguntas,on_delete=models.CASCADE)

class Estadisticas(models.Model):
    nombre_usuario_fk = models.ForeignKey(Usuarios,on_delete=models.CASCADE)
    id_cuestionario_fk = models.ForeignKey(Cuestionarios,on_delete=models.PROTECT,null=True)
    id_tema_fk = models.ForeignKey(Temas,on_delete=models.CASCADE)
    acertadas = models.IntegerField(null=False)
    falladas = models.IntegerField(null=False)
    porcentaje_acierto = models.FloatField(null=False)
    fecha_creacion = models.DateTimeField(auto_now=True)

