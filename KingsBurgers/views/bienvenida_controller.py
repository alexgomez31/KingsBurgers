from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from KingsBurgers.models.Usuario import Usuario
from KingsBurgers.models import Categoria, Producto

class BienvenidaController:
    # @staticmethod
    # def bienvenida_view(request):
    #     if request.user.is_authenticated:
    #         try:
    #             usuario = Usuario.objects.get(id=request.user.id)
    #             if usuario.tipo_usuario in ['EMPLEADO', 'ADMIN']:
    #                 return render(request, 'admin/dashboard.html', {
    #                     'usuario': usuario,
    #                 })
    #             else:
    #             # return redirect('bienvenida')
    #                 return render(request, 'bienvenida.html', {'logueado': True, 'usuario': usuario})
    #         except Usuario.DoesNotExist:
    #             pass
        
    #     return render(request, 'bienvenida.html', {'logueado': False})
    @staticmethod
    def bienvenida_view(request):
        if request.user.is_authenticated:
            try:
                usuario = Usuario.objects.get(id=request.user.id)
                categorias = Categoria.objects.all()
                productos = Producto.objects.all()
                context = {
                    'usuario': usuario,
                    'categorias': categorias,
                    'productos': productos
                }
                if usuario.tipo_usuario in ['EMPLEADO', 'ADMIN']:
                    return render(request, 'admin/dashboard.html', context)
                else:
                    return render(request, 'bienvenida.html', {'logueado': True, **context})
            except Usuario.DoesNotExist:
                pass

        categorias = Categoria.objects.all()
        productos = Producto.objects.all()
        return render(request, 'bienvenida.html', {'logueado': False, 'categorias': categorias, 'productos': productos})

  
    

        
          