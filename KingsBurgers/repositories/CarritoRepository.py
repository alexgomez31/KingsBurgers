from django.db import transaction
from KingsBurgers.models import Usuario, Carrito, CartItem, Producto


class CarritoRepository:
    @classmethod
    def obtener_carrito_activo(cls, usuario: Usuario) -> Carrito:
        """Obtiene o crea un carrito activo para el usuario"""
        carrito, created = Carrito.objects.get_or_create(
            usuario=usuario,
            estado='ACTIVO'
        )
        return carrito

    @classmethod
    @transaction.atomic
    def agregar_producto(cls, carrito: Carrito, producto: Producto, cantidad: int = 1) -> CartItem:
        """Agrega un producto al carrito o incrementa su cantidad si ya existe"""
        item, created = CartItem.objects.get_or_create(
            carrito=carrito,
            producto=producto,
            defaults={
                'cantidad': cantidad,
                'precio_unitario': producto.precio
            }
        )
        
        if not created:
            item.cantidad += cantidad
            item.save()
        
        return item

    @classmethod
    @transaction.atomic
    def eliminar_item(cls, item_id: int) -> None:
        """Elimina un item del carrito"""
        CartItem.objects.filter(id=item_id).delete()

    @classmethod
    @transaction.atomic
    def actualizar_cantidad(cls, item_id: int, cantidad: int) -> CartItem:
        """Actualiza la cantidad de un item en el carrito"""
        item = CartItem.objects.get(id=item_id)
        item.cantidad = cantidad
        item.save()
        return item

    @classmethod
    def obtener_items_carrito(cls, carrito: Carrito) -> list:
        """Obtiene todos los items del carrito con información relacionada"""
        return list(carrito.items.select_related('producto').all())