from KingsBurgers.repositories.CarritoRepository import CarritoRepository

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from KingsBurgers.services.CarritoService import CarritoService

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

