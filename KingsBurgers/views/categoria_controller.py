from django.shortcuts import render, redirect, get_object_or_404
from KingsBurgers.forms import CategoriaForm
from KingsBurgers.models import Categoria, Administrador
from django.http import JsonResponse

class CategoriaController:
# def listar_categorias(request):
#     categorias = Categoria.objects.all()
#     if request.method == 'POST':
#         form = CategoriaForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('listar_categorias')
#     else:
#         form = CategoriaForm()
#     return render(request, 'admin/categorias.html', {
#         'categorias': categorias,
#         'form': form
#     })
    def crear_categoria(request):
        if request.method == 'POST':
            form_data = request.POST.copy()
            
            # Si necesitas validar que el administrador existe
            try:
                administrador = Administrador.objects.get(id=form_data.get('administrador'))
            except Administrador.DoesNotExist:
                return JsonResponse({'error': 'Administrador no válido'}, status=400)
            
            # Crear la categoría
            categoria = Categoria(
                nombre=form_data.get('nombre'),
                descripcion=form_data.get('descripcion'),
                habilitado=form_data.get('habilitado'),
                administrador=administrador
            )
            categoria.save()
            
            return JsonResponse({'success': True})
        Administrador
        
        return JsonResponse({'error': 'Método no permitido'}, status=405)

      # Asegura que solo acepte POST
    def editar_categoria(request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            # Devolver respuesta JSON para AJAX
            return JsonResponse({'success': True, 'message': 'Categoría actualizada correctamente'})
        else:
            # Devolver errores en formato JSON
            errors = {field: errors[0] for field, errors in form.errors.items()}
            return JsonResponse({
                'success': False, 
                'message': 'Por favor verifica los datos ingresados', 
                'errors': errors
            }, status=400)

    def eliminar_categoria(request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        categoria.delete()
        return redirect('categorias')
