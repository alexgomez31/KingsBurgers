from django.db import models
from KingsBurgers.models import Usuario, Carrito

class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    carrito = models.OneToOneField(Carrito, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
