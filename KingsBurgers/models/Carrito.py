from django.db import models
from KingsBurgers.models.Usuario import Usuario

class Carrito(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('PENDIENTE', 'Pendiente de pago'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    ]

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='carritos'
    )
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='ACTIVO'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'
        ordering = ['-updated_at']

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def cantidad_items(self):
        return self.items.count()

    def vaciar(self):
        self.items.all().delete()