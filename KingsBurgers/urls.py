from django.contrib import admin
from django.urls import path
from KingsBurgers.views.usuario_controller import UsuarioController
from KingsBurgers.views.bienvenida_controller import BienvenidaController
from KingsBurgers.views.vistas_admin_empleado_controller import VistasAdminEmpleadoController
from KingsBurgers.views.categoria_controller import CategoriaController
from django.contrib.auth.views import LogoutView

urlpatterns = [

    # vistas
    path('', BienvenidaController.bienvenida_view, name='bienvenida'),
    path('admin/panel/', VistasAdminEmpleadoController.panel_admin_view, name='panel_admin'),
    path('admin/usuarios/', VistasAdminEmpleadoController.panel_gestion_usuarios_view, name='gestion_usuarios'),
    path('admin/dashboard/', VistasAdminEmpleadoController.dashborard_view, name='dashboard'),
    path('admin/categorias/', VistasAdminEmpleadoController.panel_gestion_categorias_view, name='categorias'),
    path('admin/productos/', VistasAdminEmpleadoController.panel_gestion_productos_view, name='productos'),
    path('admin/inventario/', VistasAdminEmpleadoController.panel_gestion_inventario_view, name='inventario'),


    # categorias
    path('categorias/crear/', CategoriaController.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:pk>/', CategoriaController.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:pk>/', CategoriaController.eliminar_categoria, name='eliminar_categoria'),



    # cuenta
    path('registro/', UsuarioController.registro_usuario, name='registro_usuario'),
    path('login/', UsuarioController.login_usuario, name='login'),
    path('logout/', UsuarioController.logout_usuario, name='logout'),
]