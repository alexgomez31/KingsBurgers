from django.db import models
from KingsBurgers.models.Pedido import Pedido

class Pago(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50)
    metodo = models.CharField(max_length=50)
    id_externo = models.CharField(max_length=100)  
    fecha_pago = models.DateTimeField(auto_now_add=True)
