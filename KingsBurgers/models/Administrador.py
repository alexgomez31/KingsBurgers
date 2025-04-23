from django.db import models
from KingsBurgers.models.Usuario import Usuario

class Administrador(models.Model):
    id = models.AutoField(primary_key=True)  # Campo explícito autoincremental
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='administrador')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def crear_desde_usuario(cls, usuario, datos):
        admin = cls(usuario=usuario)
        admin.save()
        return admin

    def acciones_post_registro(self):
        print(f"Administrador {self.usuario.nombre} registrado. Otorgando todos los permisos.")

    def cargar_preferencias(self):
        print(f"Cargando panel de control completo para {self.usuario.nombre}")

    def obtener_url_dashboard(self):
        return "/admin/dashboard/"

    def gestionar_usuarios(self):
        print(f"Administrador {self.usuario.nombre} gestionando usuarios del sistema")
        return True

    def generar_reporte(self, tipo_reporte):
        print(f"Administrador {self.usuario.nombre} generando reporte de {tipo_reporte}")
        return True