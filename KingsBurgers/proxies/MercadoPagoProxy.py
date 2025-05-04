# proxies/MercadoPagoProxy.py
import mercadopago

class MercadoPagoProxy:
    def __init__(self, access_token):
        self.client = mercadopago.SDK(access_token)

    def crear_preferencia(self, carrito, success_url, failure_url):
        items = []
        for item in carrito.cartitem_set.all():
            items.append({
                "title": item.producto.nombre,
                "quantity": item.cantidad,
                "unit_price": float(item.precio_unitario),
            })

        preference_data = {
            "items": items,
            "back_urls": {
                "success": success_url,
                "failure": failure_url,
            },
            "auto_return": "approved"
        }

        preference = self.client.preference().create(preference_data)
        return preference["response"]
