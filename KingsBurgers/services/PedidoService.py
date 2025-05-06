from KingsBurgers.models import Pedido, Pago, Usuario, Carrito

class PedidoService:
    @staticmethod
    def registrar_pedido(usuario: Usuario, carrito: Carrito, datos_pago: dict) -> Pedido:
        carrito.estado = 'PAGADO'
        carrito.save()

        pedido = Pedido.objects.create(usuario=usuario, carrito=carrito)

        Pago.objects.create(
            pedido=pedido,
            monto=carrito.total,
            estado=datos_pago.get('status', 'pendiente'),
            metodo='MercadoPago',
            id_externo=datos_pago.get('payment_id', '')
        )

        return pedido
