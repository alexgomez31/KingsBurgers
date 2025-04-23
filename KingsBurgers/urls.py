from django.contrib import admin
from django.urls import path
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
]