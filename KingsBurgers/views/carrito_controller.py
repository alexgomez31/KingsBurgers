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
        adiciones = request.POST.get('adiciones', '[]')
        bebidas = request.POST.get('bebidas', '[]')
        descripcion = request.POST.get('descripcion', '')

        import json
        adiciones_ids = json.loads(adiciones)
        bebidas_ids = json.loads(bebidas)

        servicio = CarritoService(request.user)
        resultado = servicio.agregar_producto(producto_id, cantidad, adiciones_ids, bebidas_ids, descripcion)

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
            Prefetch('items', queryset=CartItem.objects.select_related('producto__categoria'))
        )

        resultado = []

        for carrito in carritos_pagados:
            try:
                cliente = Cliente.objects.get(usuario=carrito.usuario)
            except Cliente.DoesNotExist:
                cliente = None

            items_dict = {}
            adicionales_temp = []

            for item in carrito.items.all():
                if item.adicionales_id is None:
                    items_dict[item.id] = {
                        'producto_id': item.producto.id,
                        'nombre': item.producto.nombre,
                        'descripcion': item.producto.descripcion,
                        'imagen': item.producto.imagen.url if item.producto.imagen else None,
                        'cantidad': item.cantidad,
                        'recomendacion_cliente': item.descripcion,
                        'adiciones': []
                    }
                else:
                    adicionales_temp.append(item)

            # Asociar adicionales
            for adicional in adicionales_temp:
                if adicional.adicionales_id in items_dict:
                    items_dict[adicional.adicionales_id]['adiciones'].append({
                        'producto_id': adicional.producto.id,
                        'nombre': adicional.producto.nombre,
                        'descripcion': adicional.producto.descripcion,
                        'categoria': adicional.producto.categoria.nombre if adicional.producto.categoria else None
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
                'productos': list(items_dict.values())
            })

        return JsonResponse({'carritos': resultado})
    

    
    @require_POST
    @login_required
    def obtener_productos_categoria(request):
        categoria = request.POST.get('categoria')
        
        if not categoria:
            return JsonResponse({'success': False, 'error': 'Categoría no especificada'})
        
        servicio = CarritoService(request.user)
        productos = servicio.obtener_productos_habilitados(categoria)
        
        return JsonResponse({'success': True, 'productos': productos})
