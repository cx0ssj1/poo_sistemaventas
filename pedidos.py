from productos import ItemProductos

class Pedido:
    def __init__(self, productos):
        self.productos = productos
        self.items = {
            "cuadernos": [],
            "lapices": [],
            "varios": []
        }
        self.estado = "Pendiente"
    def agregar_item(self, item):
        if isinstance(item, ItemProductos):
            if item.tipo == "Cuadernos":
                self.items["cuadernos"].append(item)
            elif item.tipo == "Lapices":
                self.items["lapices"].append(item)
            elif item.tipo == "Varios":
                self.items["varios"].append(item)
    def calcular_total(self):
        total = 0
        for categoria in self.items.values():
            for item in categoria:
                total += item.calcular_subtotal()
        return round(total, 2)
    def cambiar_estado(self, nuevo_estado):
        estados_validos = ["Pendiente", "En Preparación", "Listo", "Entregado"]
        if nuevo_estado in estados_validos:
            self.estado = nuevo_estado
            return True
        return False
    def obtener_resumen(self):
        resumen = []
        for categoria, items in self.items.items():
            if items:
                resumen.append(f"\n{categoria.replace('_',' ').title()}:")
                for item in items:
                    resumen.append(f"- {item.nombre} x{item.cantidad}: ${item.calcular_subtotal(): .2f}")
        resumen.append(f"\nTotal: ${self.calcular_total(): .2f}")
        return "\n".join(resumen)
    def cancelar_pedido(self):
        self.estado = "Cancelado"
        self.items = {
            "cuadernos": [],
            "lapices": [],
            "varios": []
        }
        return f"pedido cancelado {self.pedidos_activos}"