from KingsBurgers.repositories.CarritoRepository import CarritoRepository

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from KingsBurgers.services.CarritoService import CarritoService
from KingsBurgers.models import Carrito, Producto,Cliente, Usuario
from django.views.decorators.http import require_GET
from django.db.models import Prefetch
from KingsBurgers.models.CarritoItem import CartItem 

class CarritoController:

    @login_required
    @require_POST
    def agregar_producto(request):
        producto_id = int(request.POST.get('producto_id'))
        cantidad = int(request.POST.get('cantidad', 1))

        servicio = CarritoService(request.user)
        resultado = servicio.agregar_producto(producto_id, cantidad)

        return JsonResponse(resultado)

    @require_POST
    @login_required
    def actualizar_cantidad(request):
        item_id = int(request.POST.get('item_id'))
        cantidad = int(request.POST.get('cantidad'))

        servicio = CarritoService(request.user)
        resultado = servicio.actualizar_cantidad(item_id, cantidad)

        return JsonResponse(resultado)

    @require_POST
    @login_required
    def obtener_carrito(request):
        servicio = CarritoService(request.user)
        resultado = servicio.obtener_estado_carrito()
        return JsonResponse(resultado)

    
    @require_POST
    @login_required
    def vaciar(request):
        servicio = CarritoService(request.user)
        servicio.vaciar_carrito()
        return JsonResponse({'success': True, 'message': 'Carrito vaciado correctamente'})
    
    @require_POST
    @login_required
    def eliminar_item(request):
        item_id = int(request.POST.get('item_id'))

        servicio = CarritoService(request.user)
        resultado = servicio.actualizar_cantidad(item_id, 0)  # Ya maneja la eliminación si cantidad <= 0

        return JsonResponse(resultado)

    @require_GET
    def getCarritoEmpleado(request):
        carritos_pagados = Carrito.objects.filter(estado='PAGADO').select_related('usuario').prefetch_related(
            Prefetch('items', queryset=CartItem.objects.select_related('producto'))
        )

        resultado = []

        for carrito in carritos_pagados:
            try:
                cliente = Cliente.objects.get(usuario=carrito.usuario)
            except Cliente.DoesNotExist:
                cliente = None

            items = []
            for item in carrito.items.all():
                items.append({
                    'producto_id': item.producto.id,
                    'nombre': item.producto.nombre,
                    'descripcion': item.producto.descripcion,
                    'imagen': item.producto.imagen.url if item.producto.imagen else None,
                    'cantidad': item.cantidad,
                })

            resultado.append({
                'carrito_id': carrito.id,
                'estado': carrito.estado,
                'fecha': carrito.created_at,
                'usuario': {
                    'id': carrito.usuario.id,
                    'nombre': carrito.usuario.nombre,
                    'correo': carrito.usuario.correo,
                    'tipo_usuario': carrito.usuario.tipo_usuario,
                },
                'cliente': {
                    'telefono': cliente.telefono if cliente else None,
                    'direccion': cliente.direccion if cliente else None,
                },
                'productos': items
            })

        return JsonResponse({'carritos': resultado})