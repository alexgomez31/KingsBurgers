from django.contrib import admin
from django.urls import path
from KingsBurgers.views.carrito_controller import CarritoController
from KingsBurgers.views.pago_controller import PagoController
from KingsBurgers.views.usuario_controller import UsuarioController
from KingsBurgers.views.bienvenida_controller import BienvenidaController
from KingsBurgers.views.vistas_admin_empleado_controller import VistasAdminEmpleadoController
from KingsBurgers.views.categoria_controller import CategoriaController
from KingsBurgers.views.inventario_controller import InventarioController
from KingsBurgers.views.producto_controller import ProductoController
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # vistas
    path('', BienvenidaController.bienvenida_view, name='bienvenida'),
    path('admin/panel/', VistasAdminEmpleadoController.panel_admin_view, name='panel_admin'),
    path('admin/usuarios/', VistasAdminEmpleadoController.panel_gestion_usuarios_view, name='gestion_usuarios'),
    path('admin/dashboard/', VistasAdminEmpleadoController.dashborard_view, name='dashboard'),
    path('admin/dashboardempleado/', VistasAdminEmpleadoController.dashborard_view, name='dashboardempleado'),
    path('admin/categorias/', VistasAdminEmpleadoController.panel_gestion_categorias_view, name='categorias'),
    path('admin/productos/', VistasAdminEmpleadoController.panel_gestion_productos_view, name='productos'),
    path('admin/inventario/', VistasAdminEmpleadoController.panel_gestion_inventario_view, name='inventario'),


    # categorias
    path('categorias/crear/', CategoriaController.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:pk>/', CategoriaController.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:pk>/', CategoriaController.eliminar_categoria, name='eliminar_categoria'),

    #inventario
    path('admin/inventario/crear/', InventarioController.crear_inventario, name='crear_inventario'),
    path('admin/inventario/editar/<int:id>/', InventarioController.editar_inventario, name='editar_inventario'),
    path('admin/inventario/eliminar/<int:id>/', InventarioController.eliminar_inventario, name='eliminar_inventario'),

    #productos
     # URLs para la gestión de productos
    path('admin/productos/crear/', ProductoController.crear_producto, name='crear_producto'),
    path('admin/productos/editar/<int:id>/', ProductoController.editar_producto, name='editar_producto'),
    path('admin/productos/eliminar/<int:id>/', ProductoController.eliminar_producto, name='eliminar_producto'),
    path('admin/productos/<int:id>/json/', ProductoController.obtener_producto_json, name='producto_json'),

    path('registro/', UsuarioController.registro_usuario, name='registro_usuario'),
    path('login/', UsuarioController.login_usuario, name='login'),
    path('logout/', UsuarioController.logout_usuario, name='logout'),

    # carrito
    path('carrito/agregar/', CarritoController.agregar_producto, name='carrito_agregar'),
    path('carrito/actualizar/', CarritoController.actualizar_cantidad, name='carrito_actualizar'),
    path('carrito/estado/', CarritoController.obtener_carrito, name='carrito_estado'),
    path('carrito/vaciar/', CarritoController.vaciar, name='carrito_vaciar'),
    path('carrito/eliminar/', CarritoController.eliminar_item, name='carrito_eliminar_item'),

    #pagos
    path('carrito/generar-preferencia/', PagoController.generar_preferencia_pago, name='generar_preferencia_pago'),
    path('pago/exito/', PagoController.pago_exitoso, name='pago_exitoso'),
    path('pago/error/', PagoController.pago_error, name='pago_error'),


    # vista empleado carritos pagos
    path('carritos-pagados/', CarritoController.getCarritoEmpleado, name='carritos_pagados'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
