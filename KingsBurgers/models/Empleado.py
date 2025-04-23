from django.db import models
from KingsBurgers.models.Usuario import Usuario

class Empleado(models.Model):
    id = models.AutoField(primary_key=True)  # Campo explícito autoincremental
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='empleado')
    fecha_contrato = models.DateField()
    habilitado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def crear_desde_usuario(cls, usuario, datos):
        empleado = cls(
            usuario=usuario,
            fecha_contrato=datos.get('fecha_contrato'),
            habilitado=datos.get('habilitado', True)
        )
        empleado.save()
        return empleado

    def acciones_post_registro(self):
        print(f"Empleado {self.usuario.nombre} registrado. Asignando tareas iniciales.")

    def cargar_preferencias(self):
        print(f"Cargando asignaciones para {self.usuario.nombre}")

    def obtener_url_dashboard(self):
        return "/empleado/dashboard/"