from django import forms
from KingsBurgers.models.Usuario import Usuario
from KingsBurgers.models import Categoria, Producto, Inventario

class RegistroUsuarioForm(forms.Form):
    TIPO_USUARIO_CHOICES = [
        ('CLIENTE', 'Cliente'),
        ('EMPLEADO', 'Empleado'),
        ('ADMIN', 'Administrador'),
    ]
    
    nombre = forms.CharField(max_length=100, required=True)
    correo = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True) 
    confirmar_password = forms.CharField(widget=forms.PasswordInput, required=True)  
    tipo_usuario = forms.ChoiceField(choices=TIPO_USUARIO_CHOICES, required=True)
    telefono = forms.CharField(max_length=15, required=False)
    direccion = forms.CharField(widget=forms.Textarea, required=False)
    fecha_contrato = forms.DateField(required=False)
    codigo_admin = forms.CharField(max_length=10, required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar_password = cleaned_data.get("confirmar_password")
        tipo_usuario = cleaned_data.get("tipo_usuario")

        if password != confirmar_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        if tipo_usuario == 'ADMIN' and not cleaned_data.get("codigo_admin"):
            raise forms.ValidationError("El código de administrador es obligatorio.")

        return cleaned_data
    
class LoginForm(forms.Form):
    correo = forms.EmailField(label='Correo electrónico')
    contraseña = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    print("LoginForm initialized", correo, contraseña)

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'habilitado', 'administrador']