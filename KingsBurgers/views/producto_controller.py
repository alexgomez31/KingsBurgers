from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from KingsBurgers.models import Producto, Categoria, Usuario
from KingsBurgers.forms import ProductoForm
from django.conf import settings
import os


class ProductoController:
    
    @login_required
    def crear_producto(request):
        if request.method == 'POST':
            form = ProductoForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Producto creado correctamente')
            else:
                messages.error(request, 'Error al crear el producto')
        return redirect('productos')
    
    @login_required
    def editar_producto(request, id):
        producto = get_object_or_404(Producto, id=id)
        if request.method == 'POST':
            form = ProductoForm(request.POST, request.FILES, instance=producto)
            if form.is_valid():
                if 'imagen' in request.FILES:
                    # Guardar sin imagen primero para liberar el archivo
                    if producto.imagen:
                        ruta_anterior = os.path.join(settings.MEDIA_ROOT, producto.imagen.name)
                        producto.imagen = None
                        producto.save()

                        # Ahora eliminar la imagen
                        if os.path.exists(ruta_anterior):
                            try:
                                os.remove(ruta_anterior)
                            except PermissionError:
                                messages.warning(request, 'La imagen anterior no se pudo eliminar porque está en uso.')

                form.save()
                messages.success(request, 'Producto actualizado correctamente')
            else:
                messages.error(request, 'Error al actualizar el producto')
            return redirect('productos')
        else:
            form = ProductoForm(instance=producto)
        return render(request, 'editar_producto.html', {'form': form, 'producto': producto})
    
    @login_required
    def eliminar_producto(request, id):
        try:
            producto = get_object_or_404(Producto, id=id)
            producto.delete()
            messages.success(request, 'Producto eliminado correctamente')
        except Exception as e:
            messages.error(request, f'Error al eliminar el producto: {str(e)}')
        return redirect('productos')
    
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
    def obtener_producto_json(request, id):
        """
        Endpoint para obtener datos de un producto específico en formato JSON
        (Útil para cargar datos en modal de edición vía AJAX)
        """
        from django.http import JsonResponse
        try:
            producto = get_object_or_404(Producto, id=id)
            data = {
                'id': producto.id,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'precio': float(producto.precio),
                'categoria': producto.categoria.id,
                'habilitado': producto.habilitado,
                'imagen_url': producto.imagen.url if producto.imagen else None,
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)