from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from KingsBurgers.models import Inventario, Producto, Usuario
from KingsBurgers.forms import InventarioForm

class InventarioController:
    
    @login_required
    def crear_inventario(request):
        if request.method == 'POST':
            form = InventarioForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Producto agregado al inventario correctamente')
            else:
                messages.error(request, 'Error al agregar el producto al inventario')
        return redirect('inventario')
    
    @login_required
    def editar_inventario(request, id):
        inventario = get_object_or_404(Inventario, id=id)
        
        if request.method == 'POST':
            form = InventarioForm(request.POST, instance=inventario)
            if form.is_valid():
                form.save()
                messages.success(request, 'Inventario actualizado correctamente')
            else:
                messages.error(request, 'Error al actualizar el inventario')
        return redirect('inventario')
    
    @login_required
    def eliminar_inventario(request, id):
        try:
            inventario = get_object_or_404(Inventario, id=id)
            inventario.delete()
            messages.success(request, 'Producto eliminado del inventario correctamente')
        except Exception as e:
            messages.error(request, f'Error al eliminar el producto: {str(e)}')
        return redirect('inventario')
    
    @login_required
    def panel_gestion_inventario_view(request):
        try:
            usuario = Usuario.objects.get(id=request.user.id)
            
            if usuario.tipo_usuario not in ['EMPLEADO', 'ADMIN']:
                messages.warning(request, 'No tienes permisos para acceder a esta sección')
                return redirect('bienvenida')
            
            inventarios = Inventario.objects.all().order_by('-id')
            productos = Producto.objects.all()
            form = InventarioForm()
            
            return render(request, 'admin/inventario.html', {
                'usuario': usuario,
                'inventarios': inventarios,
                'form': form,
                'productos': productos
            })
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')
            return redirect('bienvenida')
    
    @login_required
    def obtener_inventario_json(request, id):
        """
        Endpoint para obtener datos de un inventario específico en formato JSON
        (Útil para cargar datos en modal de edición vía AJAX)
        """
        from django.http import JsonResponse
        try:
            inventario = get_object_or_404(Inventario, id=id)
            data = {
                'id': inventario.id,
                'producto': inventario.producto.id,
                'cantidad_disponible': inventario.cantidad_disponible,
                'desde': inventario.desde.strftime('%Y-%m-%dT%H:%M'),
                'hasta': inventario.hasta.strftime('%Y-%m-%dT%H:%M'),
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)