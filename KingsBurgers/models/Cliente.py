from django.db import models
from KingsBurgers.models.Usuario import Usuario

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)  # Campo explícito autoincremental
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='cliente')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def crear_desde_usuario(cls, usuario, datos):
        cliente = cls(
            usuario=usuario,
            telefono=datos.get('telefono', ''),
            direccion=datos.get('direccion', '')
        )
        cliente.save()
        return cliente

    def acciones_post_registro(self):
        print(f"Cliente {self.usuario.nombre} registrado. Enviando catálogo de productos.")

    def cargar_preferencias(self):
        print(f"Cargando historial de compras para {self.usuario.nombre}")

    def obtener_url_dashboard(self):
        return "/cliente/dashboard/"