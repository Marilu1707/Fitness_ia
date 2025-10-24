from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    NIVELES = [
        ('bajo', 'Bajo'),
        ('medio', 'Medio'),
        ('alto', 'Alto'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    edad = models.PositiveIntegerField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.DecimalField(max_digits=4, decimal_places=2)
    nivel = models.CharField(max_length=10, choices=NIVELES)
    dias_entrenamiento = models.PositiveIntegerField(default=3)

    def __str__(self):
        return f"{self.usuario.username} ({self.edad} años)"

class Objetivo(models.Model):

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100)
    peso_deseado = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    dias_entrenamiento = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.usuario.username} - {self.tipo}"


class Progreso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    imagen = models.ImageField(upload_to='progreso/', blank=True, null=True)
    peso_actual = models.FloatField(null=True, blank=True)
    horas = models.FloatField(default=0)

    class Meta:
        ordering = ["-fecha", "-id"]

    def __str__(self):
        return f"Progreso de {self.usuario.username} - {self.fecha}"


class Profesional(models.Model):
    TIPO_CHOICES = [
        ('entrenador', 'Entrenador'),
        ('nutricionista', 'Nutricionista'),
    ]

    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    ubicacion = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='profesionales/', blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"
