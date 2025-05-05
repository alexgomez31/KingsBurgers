
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
                "success_url": "https://e3c5-190-90-100-68.ngrok-free.app/pago/exito/",
                "failure_url": "https://e3c5-190-90-100-68.ngrok-free.app/pago/error/"
            }

            data = proxy.crear_preferencia(carrito, **urls)
            return JsonResponse(data)
        except Exception as e:
            print("Error en generar_preferencia_pago:", e)
            return JsonResponse({"error": str(e)}, status=500)
  
    @login_required
    @require_GET
    def pago_exitoso(request):
        payment_id = request.GET.get("payment_id")
        status = request.GET.get("status")

        # Consultar el estado actualizado del pago
        proxy = MercadoPagoProxy()
        payment_data = proxy.consultar_pago(payment_id)
        status_actual = payment_data.get("status", status)  # El estado actualizado del pago

        carrito = CarritoRepository.obtener_carrito_activo(request.user)
        PedidoService.registrar_pedido(request.user, carrito, {
            "payment_id": payment_id,
            "status": status_actual
        })

        return redirect('bienvenida')

    @staticmethod
    def pago_error(request):
        return render(request, 'bienvenida.html')

 
