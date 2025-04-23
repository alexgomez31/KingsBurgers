from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Usuario(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('CLIENTE', 'Cliente'),
        ('EMPLEADO', 'Empleado'),
        ('ADMIN', 'Administrador'),
    ]

    id = models.AutoField(primary_key=True)  # Campo explícito autoincremental
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Contraseña cifrada
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre']

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def verify_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @classmethod
    def registrar_usuario(cls, datos, tipo):
        if not cls._validar_datos_comunes(datos):
            return None, "Datos incompletos o inválidos"

        usuario = cls(
            nombre=datos['nombre'],
            correo=datos['correo'],
            tipo_usuario=tipo
        )
        usuario.set_contraseña(datos['contraseña'])

        try:
            usuario.save()

            if tipo == 'CLIENTE':
                perfil = Cliente.crear_desde_usuario(usuario, datos)
            elif tipo == 'EMPLEADO':
                perfil = Empleado.crear_desde_usuario(usuario, datos)
            elif tipo == 'ADMIN':
                perfil = Administrador.crear_desde_usuario(usuario, datos)
            else:
                usuario.delete()
                return None, "Tipo de usuario no válido"

            cls._enviar_correo_bienvenida(usuario)
            perfil.acciones_post_registro()
            return usuario, "Usuario registrado correctamente"
        except Exception as e:
            if usuario.pk:
                usuario.delete()
            return None, f"Error al registrar: {str(e)}"

    @staticmethod
    def _validar_datos_comunes(datos):
        return (
            datos.get('nombre') and
            datos.get('correo') and
            datos.get('contraseña')
        )

    @staticmethod
    def _enviar_correo_bienvenida(usuario):
        print(f"Enviando correo de bienvenida a {usuario.correo}")

    @staticmethod
    def iniciar_sesion(correo, password):
        try:
            usuario = Usuario.objects.get(correo=correo)
            print(f"Usuario encontrado: {usuario.nombre}")
            if not usuario.verify_password(password):
                return None, "Contraseña incorrecta"
            return usuario, None
        except Usuario.DoesNotExist:
            return None, "Usuario no encontrado"