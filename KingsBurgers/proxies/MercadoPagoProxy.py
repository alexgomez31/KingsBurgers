import mercadopago
from django.conf import settings

class MercadoPagoProxy:
    def __init__(self):
       
        self.client = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    def crear_preferencia(self, carrito, success_url, failure_url):
        
        items_data = []
        productos = []
        for item in carrito.items.all():
            items_data.append({
                "title": item.producto.nombre,
                "quantity": item.cantidad,
                "unit_price": float(item.precio_unitario),
            })
            productos.append(item.producto.nombre)

       
        preference_data = {
            "items": items_data,
            "back_urls": {
                "success": success_url,
                "failure": failure_url,
            },
            "payer": {
                "name": carrito.usuario.nombre,
                "email": carrito.usuario.correo,
            },
            
        }

      
        resultado = self.client.preference().create(preference_data)
        response = resultado.get("response", {})

        
        init_point = (
            response.get("sandbox_init_point") if settings.DEBUG
            else response.get("init_point")
        )
        if not init_point:
            raise Exception("No se encontró init_point en la respuesta de MercadoPago")

        total = float(carrito.total)

       
        return {
            "init_point": init_point,
            "productos": productos,
            "total": total,
        }
