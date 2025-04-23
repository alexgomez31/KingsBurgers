from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from KingsBurgers.models.Usuario import Usuario

class BienvenidaController:
    @staticmethod
    def bienvenida_view(request):
        if request.user.is_authenticated:
            try:
                usuario = Usuario.objects.get(id=request.user.id)
                if usuario.tipo_usuario in ['EMPLEADO', 'ADMIN']:
                    return render(request, 'admin/dashboard.html', {
                        'usuario': usuario,
                    })
                else:
                # return redirect('bienvenida')
                    return render(request, 'bienvenida.html', {'logueado': True, 'usuario': usuario})
            except Usuario.DoesNotExist:
                pass
        
        return render(request, 'bienvenida.html', {'logueado': False})

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
          