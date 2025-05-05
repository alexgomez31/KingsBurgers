# views/pago_controller.py

from django.views.decorators.http import require_POST, require_GET
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse

from KingsBurgers.services.PedidoService import PedidoService
from KingsBurgers.repositories.CarritoRepository import CarritoRepository
from KingsBurgers.proxies.MercadoPagoProxy import MercadoPagoProxy


class PagoController:

   
    @login_required
    @require_POST
    def generar_preferencia_pago(request):
        try:
            carrito = CarritoRepository.obtener_carrito_activo(request.user)
            proxy = MercadoPagoProxy()
            urls = {
                "success_url": request.build_absolute_uri("/pago/exito/"),
                "failure_url": request.build_absolute_uri("/pago/error/")
            }
            data = proxy.crear_preferencia(carrito, **urls)
            return JsonResponse(data)
        except Exception as e:
            # Loggea e imprime e para depuración
            print("Error en generar_preferencia_pago:", e)
            return JsonResponse({"error": str(e)}, status=500)
  
    @login_required
    @require_GET
    def pago_exitoso(request):
        payment_id = request.GET.get("payment_id")
        status = request.GET.get("status")

        carrito = CarritoRepository.obtener_carrito_activo(request.user)
        PedidoService.registrar_pedido(request.user, carrito, {
            "payment_id": payment_id,
            "status": status
        })

        return redirect("pagina_confirmacion")

    @staticmethod
    def pago_error(request):
        return render(request, 'pago_error.html')

    @staticmethod
    def pagina_confirmacion(request):
        return render(request, 'pago_exito.html')
