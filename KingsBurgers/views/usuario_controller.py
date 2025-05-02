from django.shortcuts import render, redirect
from django.contrib.auth import login
from KingsBurgers.forms import RegistroUsuarioForm, LoginForm
from KingsBurgers.models import Usuario, Cliente, Empleado, Administrador
from django.contrib.auth import logout


class UsuarioController:
    @staticmethod
    def registro_usuario(request):
  
        if request.method == 'POST':
            form = RegistroUsuarioForm(request.POST)
            if form.is_valid():
                datos = form.cleaned_data
                tipo_usuario = datos['tipo_usuario']

                usuario = Usuario(
                    nombre=datos['nombre'],
                    correo=datos['correo'],
                    tipo_usuario=tipo_usuario
                )
                usuario.set_password(datos['password'])
                usuario.save()
                print(f"Usuario creado: {usuario.tipo_usuario}")
                try:
                    if tipo_usuario == 'CLIENTE':
                        Cliente.crear_desde_usuario(usuario, datos)
                        return redirect('bienvenida') 
                    elif tipo_usuario == 'EMPLEADO':
                        Empleado.crear_desde_usuario(usuario, datos)
                        return redirect('dashboard') 
                    elif tipo_usuario == 'ADMIN':
                        Administrador.crear_desde_usuario(usuario, datos)
                        return redirect('dashboard') 
                except Exception as e:
                    usuario.delete()
                    return render(request, 'registration/register.html', {
                        'form': form,
                        'error': f"Error al crear el perfil: {str(e)}"
                    })
        else:
            form = RegistroUsuarioForm()
            
        return render(request, 'registration/register.html', {'form': form})

    @staticmethod
    def login_usuario(request):
        if request.method == 'POST':
            form = LoginForm(request.POST)
            print(f"Form data: {form.data}")
            
            if form.is_valid():
                print("Form is valid")
                correo = form.cleaned_data['correo']
                password = form.cleaned_data['contraseña']
                
                usuario, mensaje = Usuario.iniciar_sesion(correo, password)
                print(f"Usuario: {usuario}, Mensaje: {mensaje}")
                
                if usuario:
                    login(request, usuario)
                    try:
                        redirecciones = {
                            'CLIENTE': 'bienvenida',
                            'EMPLEADO': 'dashboard',
                            'ADMIN': 'dashboard',
                        }
                        ruta = redirecciones.get(usuario.tipo_usuario, 'pagina_no_autorizada')
                        return redirect(ruta)
                    except Exception as e:
                        return render(request, 'registration/login.html', {
                            'form': form,
                            'error': f"Ocurrió un error al redirigir: {str(e)}"
                        })
                else:
                    return render(request, 'registration/login.html', {
                        'form': form,
                        'error': mensaje
                    })
            else:
                print("Errores del formulario:", form.errors)
                return render(request, 'registration/login.html', {'form': form})
        
        else:
            form = LoginForm()
        
        return render(request, 'registration/login.html', {'form': form})

    @staticmethod
    def logout_usuario(request):
        logout(request)
        return redirect('login')