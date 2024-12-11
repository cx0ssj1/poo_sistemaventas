from productos import Productos
from pedidos import Pedido

class Tienda:
    def __init__(self):
        self.clientes = []
        self.pedidos_activos = []
        self.productos = Productos()
        self._inicializar_productos()
    def _inicializar_productos(self):
        self.productos.agregar_cuadernos("Cuaderno Personalizado", 12000)
        self.productos.agregar_cuadernos("Cuaderno para dibujar", 8000)
        self.productos.agregar_lapices("Lapiz multicolor", 2000)
        self.productos.agregar_lapices("Lapiz con diseño", 1000)
        self.productos.agregar_varios("Papel de regalo Disney", 1000)
        self.productos.agregar_varios("Bolsa de regalo", 400)
    def crear_pedido(self, cliente, pedido):
        self.pedidos_activos.append(pedido)
        cliente.asignar_pedido(pedido)
        return pedido