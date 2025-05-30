from django.db import models
from .Producto import Producto

class Inventario(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_disponible = models.IntegerField(null=True, blank=True, default=None)
    desde = models.DateTimeField(blank=True, null=True)  # Removido auto_now_add
    hasta = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
