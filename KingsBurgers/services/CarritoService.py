from KingsBurgers.models.CarritoItem import CartItem
from KingsBurgers.repositories.CarritoRepository import CarritoRepository
from KingsBurgers.models import Carrito, Usuario, Producto

class CarritoService:
    def __init__(self, usuario: Usuario):  
        self.usuario = usuario
        self.carrito = CarritoRepository.obtener_carrito_activo(usuario)

    
    def agregar_producto(self, producto_id: int, cantidad: int = 1) -> dict:
        """Agrega un producto al carrito del usuario"""
        try:
            producto = Producto.objects.get(id=producto_id, habilitado='SI')
            item = CarritoRepository.agregar_producto(self.carrito, producto, cantidad)
            
            return {
                'success': True,
                'item_id': item.id,
                'cantidad': item.cantidad,
                'subtotal': item.subtotal,
                'total': self.carrito.total,
                'cart_count': self.carrito.cantidad_items
            }
        except Producto.DoesNotExist:
            return {'success': False, 'error': 'Producto no encontrado o no disponible'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def actualizar_cantidad(self, item_id: int, cantidad: int) -> dict:
        """Actualiza la cantidad de un item en el carrito"""
        try:
            if cantidad <= 0:
                CarritoRepository.eliminar_item(item_id)
                return {
                    'success': True,
                    'action': 'deleted',
                    'total': self.carrito.total,
                    'cart_count': self.carrito.cantidad_items
                }
            
            item = CarritoRepository.actualizar_cantidad(item_id, cantidad)
            return {
                'success': True,
                'action': 'updated',
                'subtotal': item.subtotal,
                'total': self.carrito.total,
                'cart_count': self.carrito.cantidad_items
            }
        except CartItem.DoesNotExist:
            return {'success': False, 'error': 'Item no encontrado'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def obtener_estado_carrito(self) -> dict:
        """Obtiene el estado completo del carrito"""
        items = []
        total = 0.0

        for item in CarritoRepository.obtener_items_carrito(self.carrito):
            items.append({
                'id': item.id,
                'producto_id': item.producto.id,
                'nombre': item.producto.nombre,
                'imagen': item.producto.imagen.url if item.producto.imagen else None,
                'cantidad': item.cantidad,
                'precio_unitario': float(item.precio_unitario),
                'subtotal': float(item.subtotal)
            })
        
        return {
            'carrito_id': self.carrito.id,
            'estado': self.carrito.estado,
            'total': float(self.carrito.total),
            'items': items,
            'cart_count': self.carrito.cantidad_items
        }
    
    def vaciar_carrito(self) -> None:
        """Elimina todos los items del carrito"""
        self.carrito.vaciar()
    
    def cambiar_estado(self, nuevo_estado: str) -> bool:
        """Cambia el estado del carrito"""
        if nuevo_estado in dict(Carrito.ESTADO_CHOICES).keys():
            self.carrito.estado = nuevo_estado
            self.carrito.save()
            return True
        return False