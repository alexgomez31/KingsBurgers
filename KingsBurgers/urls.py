from django.contrib import admin
from django.urls import path
from KingsBurgers.views.carrito_controller import CarritoController
from KingsBurgers.views.usuario_controller import UsuarioController
from KingsBurgers.views.bienvenida_controller import BienvenidaController
from django.contrib.auth.views import LogoutView

urlpatterns = [

    # vistas
    path('', BienvenidaController.bienvenida_view, name='bienvenida'),
    path('admin/panel/', BienvenidaController.panel_admin_view, name='panel_admin'),
    path('admin/usuarios/', BienvenidaController.panel_gestion_usuarios_view, name='gestion_usuarios'),
    path('admin/dashboard/', BienvenidaController.dashborard_view, name='dashboard'),

    # cuenta
    path('registro/', UsuarioController.registro_usuario, name='registro_usuario'),
    path('login/', UsuarioController.login_usuario, name='login'),
    path('logout/', UsuarioController.logout_usuario, name='logout'),

    # carrito
    path('carrito/agregar/', CarritoController.agregar_producto, name='carrito_agregar'),
    path('carrito/actualizar/', CarritoController.actualizar_cantidad, name='carrito_actualizar'),
    path('carrito/estado/', CarritoController.obtener_carrito, name='carrito_estado'),
    path('carrito/vaciar/', CarritoController.vaciar, name='carrito_vaciar'),

]