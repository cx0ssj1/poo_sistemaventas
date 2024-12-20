class ItemProductos:
    def __init__(self, nombre, precio, cantidad=1):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
    def calcular_subtotal(self):
        return self.precio * self.cantidad

class Lapices(ItemProductos):
    def __init__(self, nombre, precio, cantidad=1):
        super().__init__(nombre, precio, cantidad)
        self.tipo = "Lapices"

class Cuadernos(ItemProductos):
    def __init__(self, nombre, precio, cantidad=1):
        super().__init__(nombre, precio, cantidad)
        self.tipo = "Cuadernos"

class Varios(ItemProductos):
    def __init__(self, nombre, precio, cantidad=1):
        super().__init__(nombre, precio, cantidad)
        self.tipo = "Varios"

class Productos:
    def __init__(self):
        self.lapices = []
        self.cuadernos = []
        self.varios = []
    def agregar_lapices(self, nombre, precio):
        lapiz = Lapices(nombre, precio)
        self.lapices.append(lapiz)  # Aquí agregamos la instancia
        return lapiz
    def buscar_por_codigo(self, codigo):
        """Busca un producto por su código único."""
        for item in self.lapices + self.cuadernos + self.varios:
            if item.codigo == codigo:
                return item
        return None

    def agregar_cuadernos(self, nombre, precio):
        cuaderno = Cuadernos(nombre, precio)
        self.cuadernos.append(cuaderno)  # Aquí agregamos la instancia
        return cuaderno

    def agregar_varios(self, nombre, precio):
        varios = Varios(nombre, precio)
        self.varios.append(varios)  # Aquí agregamos la instancia
        return varios
    def eliminar_item(self, tipo, nombre):
        if tipo == "Lapices":
            items = self.lapices
        elif tipo == "Cuadernos":
            items = self.cuadernos
        elif tipo == "Varios":
            items = self.varios
        else:
            return False
        for item in items [:]:
            if item.nombre == nombre:
                items.remove(item)
                return True
        return False
    def eliminar_lapices(self, nombre):
        return self.eliminar_item("Lapices", nombre)
    def eliminar_cuadernos(self, nombre):
        return self.eliminar_item("Cuadernos", nombre)
    def eliminar_varios(self, nombre):
        return self.eliminar_item("Varios", nombre)
    def obtener_item(self, tipo, nombre):
        if tipo == "Lapices":
            items = self.lapices
        elif tipo == "Cuadernos":
            items = self.cuadernos
        elif tipo == "Varios":
            items = self.varios
        else:
            return None
        for item in items [:]:
            if item.nombre == nombre:
                return item
        return None