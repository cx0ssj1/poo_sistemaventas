class Cliente:
    _next_id = 1
    def __init__(self):
        self.id = f"C{Cliente._next_id:03d}"
        Cliente._next_id += 1
        self.pedido_actual = None
    def asignar_pedido(self, pedido):
        self.pedido_actual = pedido
    def obtener_total_actual(self):
        return self.pedido_actual.calcular_total() if self.pedido_actual else 0
    def limpiar_pedido(self):
        self.pedido_actual = None
    @classmethod
    def reinciciar_contadors(cls):
        cls._next_id = 1