from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from KingsBurgers.models.Usuario import Usuario
from KingsBurgers.forms import InventarioForm
from django.contrib import messages

from KingsBurgers.models import Categoria, Producto , Inventario, Administrador, Empleado



class VistasAdminEmpleadoController:    
    @staticmethod
    @login_required
    def panel_admin_view(request):
        try:
            usuario = Usuario.objects.get(id=request.user.id)
            if usuario.tipo_usuario in ['EMPLEADO', 'ADMIN']:
                return render(request, 'admin/dashboard.html', {
                    'usuario': usuario,
                })
            else:
                return redirect('bienvenida')
        except Usuario.DoesNotExist:
            return redirect('bienvenida')    


    @staticmethod
    @login_required
    def panel_gestion_usuarios_view(request):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            usuario = Usuario.objects.get(id=request.user.id)
            
            if usuario.tipo_usuario not in ['EMPLEADO', 'ADMIN']:
                return redirect('bienvenida')
            
            usuarios = Usuario.objects.all()
            
            return render(request, 'admin/usuarios.html', {
                'usuario': usuario,
                'usuarios': usuarios,
            })
        except Usuario.DoesNotExist:
            return redirect('bienvenida')
        
    @staticmethod
    @login_required
    def dashborard_view(request):    
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            usuario = Usuario.objects.get(id=request.user.id)
            
            if usuario.tipo_usuario not in ['EMPLEADO', 'ADMIN']:
                return redirect('bienvenida')
            
            return render(request, 'admin/dashboard.html', {
                'usuario': usuario,
            })
        except Usuario.DoesNotExist:
            return redirect('bienvenida')
        

    @login_required
    def panel_gestion_categorias_view(request):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            usuario = Usuario.objects.get(id=request.user.id)
            
            # Verificar tipo de usuario
            if usuario.tipo_usuario not in ['EMPLEADO', 'ADMIN']:
                return redirect('bienvenida')
            
            # Obtener el ID específico según el tipo de usuario
            id_especifico = None
            tipo_especifico = None
            
            if usuario.tipo_usuario == 'ADMIN':
                try:
                    admin = Administrador.objects.get(usuario_id=usuario.id)
                    id_especifico = admin.id
                    tipo_especifico = 'admin'
                except Administrador.DoesNotExist:
                    return redirect('bienvenida')
            elif usuario.tipo_usuario == 'EMPLEADO':
                try:
                    empleado = Empleado.objects.get(usuario_id=usuario.id)
                    id_especifico = empleado.id
                    tipo_especifico = 'empleado'
                except Empleado.DoesNotExist:
                    return redirect('bienvenida')
            
            categorias = Categoria.objects.all()
            
            return render(request, 'admin/categorias.html', {
                'usuario': usuario,
                'categorias': categorias,
                'id_especifico': id_especifico,  # ID del admin o empleado
                'tipo_especifico': tipo_especifico,  # 'admin' o 'empleado'
            })
        except Usuario.DoesNotExist:
            return redirect('bienvenida')
    @login_required
    def panel_gestion_productos_view(request):
        try:
            usuario = Usuario.objects.get(id=request.user.id)
            
            if usuario.tipo_usuario not in ['EMPLEADO', 'ADMIN']:
                messages.warning(request, 'No tienes permisos para acceder a esta sección')
                return redirect('bienvenida')
            
            productos = Producto.objects.all().order_by('-id')
            categorias = Categoria.objects.all()
            
            return render(request, 'admin/productos.html', {
                'usuario': usuario,
                'productos': productos,
                'categorias': categorias,
            })
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')
            return redirect('bienvenida')
        
    @login_required
    def panel_gestion_inventario_view(request):
        try:
            usuario = Usuario.objects.get(id=request.user.id)

            if usuario.tipo_usuario not in ['EMPLEADO', 'ADMIN']:
                return redirect('bienvenida')

            inventarios = Inventario.objects.all()
            productos = Producto.objects.all()
            form = InventarioForm()

            return render(request, 'admin/inventario.html', {
                'usuario': usuario,
                'inventarios': inventarios,
                'form': form,
                'productos': productos
            })
        except Usuario.DoesNotExist:
            return redirect('bienvenida')