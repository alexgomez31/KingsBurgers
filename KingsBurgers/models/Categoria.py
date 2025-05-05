from django.db import models
from .Administrador import Administrador

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    habilitado = models.CharField(max_length=2, choices=[('SI', 'SI'), ('NO', 'NO')], default='SI')
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
