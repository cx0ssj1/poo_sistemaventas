import flet as ft
import datetime
import pandas as pd
import json
import os
from tienda import Tienda
from clientes import Cliente
from pedidos import Pedido
from fpdf import FPDF


class TiendaGUI:
    def __init__(self):
        self.tienda = Tienda()
        self.producto_seleccionado = None
        self.cantidad = 1
        self.total_parcial = 0.0
        self.lista_productos = []
        self.ventas_diarias = []
        self.total_parcial_text = ft.Text("Total parcial: CLP $0")
        self.tipos_productos = []  # Inicializar aquí
        self.cargar_tipos_productos()  # Cargar tipos de productos al iniciar
        self.cargar_productos_agregados()
        self.nuevo_tipo_input = ft.TextField(label="Nuevo Tipo de Producto")
        self.tipo_selector_eliminar = ft.Dropdown(
            label="Seleccionar Tipo para Eliminar",
            options=self.generar_lista_tipos()
        )
        self.contador_ventas = self.cargar_contador_ventas()  # Cargar contador de ventas

    def main(self, page: ft.Page):
        page.title = "Sistema de Ventas para Tienda"
        page.padding = 20
        page.theme_mode = "dark"
        
        # Configuración del tamaño de la ventana
        page.window.width = 1200  # Ancho de la ventana en píxeles
        page.window.height = 900  # Alto de la ventana en píxeles
        page.window.resizable = True  # Permitir redimensionar
        page.window.maximized = False  # No iniciar maximizada
        
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Administración Tienda",
                    content=self.crear_vista_admin(),
                    icon=ft.Icons.PERSON
                ),
                ft.Tab(
                    text="Ventas",
                    content=self.crear_vista_ventas(),
                    icon=ft.Icons.PAID_OUTLINED
                ),
            ],
            expand=1,
        )
        page.add(self.tabs)
        self.page = page

    def mostrar_mensaje(self, mensaje):
        dialog = ft.AlertDialog(title=ft.Text(mensaje))
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def crear_vista_admin(self):
        self.producto_selector_admin = ft.Dropdown(
            label="Seleccionar Producto para Eliminar",
            options=self.generar_lista_productos()
        )

        eliminar_btn = ft.ElevatedButton(
            "Eliminar Producto",
            on_click=self.eliminar_producto,
            style=ft.ButtonStyle(bgcolor=ft.Colors.RED)
        )

        # Botón para generar Excel de ventas diarias
        generar_excel_btn = ft.ElevatedButton(
            "Generar Excel de Ventas Diarias",
            on_click=self.guardar_ventas_en_excel
        )

        # Área de edición
        self.producto_selector_editar = ft.Dropdown(
            label="Seleccionar Producto para Editar",
            options=self.generar_lista_productos(),
            on_change=self.cargar_datos_producto  # Cargar datos al seleccionar
        )
        self.nombre_input_editar = ft.TextField(label="Nuevo Nombre")
        self.precio_input_editar = ft.TextField(label="Nuevo Precio")
        self.tipo_input_editar = ft.Dropdown(
            label="Nuevo Tipo de Producto",
            options=self.generar_lista_tipos()  # Cargar tipos al iniciar
        )
        editar_btn = ft.ElevatedButton("Editar Producto", on_click=self.editar_producto)

        eliminar_area = ft.Column(
            [
                ft.Text("Eliminar Productos", size=16, weight=ft.FontWeight.BOLD),
                self.producto_selector_admin,
                eliminar_btn,
            ],
            spacing=10
        )

        editar_area = ft.Column(
            [
                ft.Text("Editar Productos", size=16, weight=ft.FontWeight.BOLD),
                self.producto_selector_editar,
                self.nombre_input_editar,
                self.precio_input_editar,
                self.tipo_input_editar,  # Aquí se carga la lista de tipos
                editar_btn,
            ],
            spacing=10
        )

        # Área para agregar y eliminar tipos de productos
        agregar_tipo_btn = ft.ElevatedButton(
            "Agregar Tipo de Producto",
            on_click=self.agregar_tipo_producto
        )
        eliminar_tipo_btn = ft.ElevatedButton(
            "Eliminar Tipo de Producto",
            on_click=self.eliminar_tipo_producto
        )

        tipos_area = ft.Column(
            [
                ft.Text("Gestión de Tipos de Productos", size=16, weight=ft.FontWeight.BOLD),
                self.nuevo_tipo_input,
                agregar_tipo_btn,
                self.tipo_selector_eliminar,
                eliminar_tipo_btn,
            ],
            spacing=10
        )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Administración del Local", size=20, weight=ft.FontWeight.BOLD),
                    self.formulario_admin(),
                    ft.Row(
                        [
                            editar_area,   # Área de editar a la izquierda
                            tipos_area,    # Área de gestión de tipos en el centro
                            eliminar_area   # Área de eliminar a la derecha
                        ],
                        spacing=50,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    generar_excel_btn,  # Agregar botón para generar Excel
                ],
                spacing=10
            ),
            padding=ft.padding.only(top=30)
        )

    def cargar_datos_producto(self, e):
        producto_info = self.producto_selector_editar.value
        if not producto_info:
            self.mostrar_mensaje("Por favor seleccione un producto para editar.")
            return

        nombre_producto = producto_info.split(" (")[0]
        producto = self.tienda.productos.obtener_item("Lapices", nombre_producto) or \
                self.tienda.productos.obtener_item("Cuadernos", nombre_producto) or \
                self.tienda.productos.obtener_item("Varios", nombre_producto)

        if producto:
            # Llenar los campos con los datos actuales del producto
            self.nombre_input_editar.value = producto.nombre
            self.precio_input_editar.value = f"{producto.precio}"
            self.tipo_input_editar.value = producto.tipo
            self.page.update()
        else:
            self.mostrar_mensaje("El producto no se encontró para editar.")

    def formulario_admin(self):
        self.nombre_input = ft.TextField(label="Nombre del Producto")
        self.precio_input = ft.TextField(label="Precio del Producto")
        self.tipo_input = ft.Dropdown(
            label="Tipo de Producto",
            options=self.generar_lista_tipos() 

        )
        agregar_btn = ft.ElevatedButton("Agregar Producto", on_click=self.agregar_producto)
        return ft.Column([
            self.nombre_input,
            self.precio_input,
            self.tipo_input,
            agregar_btn
        ])
        

    def agregar_producto(self, e):
        nombre = self.nombre_input.value
        try:
            precio = float(self.precio_input.value)
        except ValueError:
            self.mostrar_mensaje("Precio inválido. Por favor ingrese un número válido.")
            return
        tipo = self.tipo_input.value
        if tipo == "Lapices":
            self.tienda.productos.agregar_lapices(nombre, precio)
        elif tipo == "Cuadernos":
            self.tienda.productos.agregar_cuadernos(nombre, precio)
        elif tipo == "Varios":
            self.tienda.productos.agregar_varios(nombre, precio)
        else:
            self.mostrar_mensaje("Tipo de producto no válido. Seleccione una opción válida.")
            return
        self.mostrar_mensaje(f"Producto '{nombre}' agregado exitosamente.")
        self.nombre_input.value = ""
        self.precio_input.value = ""
        self.tipo_input.value = None
        # Guardar productos en archivo
        self.guardar_productos_agregados()
        # Actualizar la lista de productos en el área de ventas
        self.actualizar_lista_productos()
        self.page.update()

    def eliminar_producto(self, e):
        producto_info = self.producto_selector_admin.value
        if not producto_info:
            self.mostrar_mensaje("Por favor seleccione un producto para eliminar.")
            return

        nombre_producto = producto_info.split(" (")[0]
        if self.tienda.productos.eliminar_item("Lapices", nombre_producto) or \
            self.tienda.productos.eliminar_item("Cuadernos", nombre_producto) or \
            self.tienda.productos.eliminar_item("Varios", nombre_producto):
                self.mostrar_mensaje(f"Producto '{nombre_producto}' eliminado exitosamente.")
                self.guardar_productos_agregados()
                self.actualizar_lista_productos()
                self.page.update()
        else:
            self.mostrar_mensaje("El producto no se pudo encontrar para eliminar.")

    def editar_producto(self, e):
        producto_info = self.producto_selector_editar.value
        if not producto_info:
            self.mostrar_mensaje("Por favor seleccione un producto para editar.")
            return

        nombre_producto = producto_info.split(" (")[0]
        producto = self.tienda.productos.obtener_item("Lapices", nombre_producto) or \
                    self.tienda.productos.obtener_item("Cuadernos", nombre_producto) or \
                    self.tienda.productos.obtener_item("Varios", nombre_producto)

        if not producto:
            self.mostrar_mensaje("El producto no se encontró para editar.")
            return

        nuevo_nombre = self.nombre_input_editar.value or producto.nombre
        nuevo_precio = float(self.precio_input_editar.value) if self.precio_input_editar.value else producto.precio
        nuevo_tipo = self.tipo_input_editar.value or producto.tipo

        # Actualizar valores
        producto.nombre = nuevo_nombre
        producto.precio = nuevo_precio
        producto.tipo = nuevo_tipo

        self.mostrar_mensaje(f"Producto '{nombre_producto}' actualizado exitosamente.")
        self.guardar_productos_agregados()
        self.actualizar_lista_productos()
        self.page.update()


    def guardar_productos_agregados(self):
        productos = []
        for producto in self.tienda.productos.lapices + self.tienda.productos.cuadernos + self.tienda.productos.varios:
            productos.append({
                "nombre": producto.nombre,
                "precio": producto.precio,
                "tipo": producto.tipo
            })
        # Guardar en un archivo JSON
        with open("productos.json", "w", encoding="UTF-8") as archivo:
            json.dump(productos, archivo, indent=4)

    def cargar_productos_agregados(self):
        try:
            # Limpiar las listas antes de cargar
            self.tienda.productos.lapices.clear()
            self.tienda.productos.cuadernos.clear()
            self.tienda.productos.varios.clear()

            # Leer el archivo JSON
            with open("productos.json", "r", encoding="UTF-8") as archivo:
                productos = json.load(archivo)
                for producto in productos:
                    nombre = producto["nombre"]
                    precio = float(producto["precio"])
                    tipo = producto["tipo"]
                    if tipo == "Lapices":
                        self.tienda.productos.agregar_lapices(nombre, precio)
                    elif tipo == "Cuadernos":
                        self.tienda.productos.agregar_cuadernos(nombre, precio)
                    elif tipo == "Varios":
                        self.tienda.productos.agregar_varios(nombre, precio)
        except FileNotFoundError:
            pass  # Si no existe el archivo, no se hace nada
        
    def crear_vista_ventas(self):
        self.lista_ventas = []  # Lista para almacenar productos vendidos
        return ft.Container(
            content=ft.Column([
                ft.Text("Gestión de Ventas", size=20, weight=ft.FontWeight.BOLD),
                self.formulario_venta(),
                self.crear_lista_ventas(),  # Nueva función para mostrar la lista de ventas
                self.boton_finalizar_venta()  # Botón para finalizar la venta
            ]),
            padding=ft.padding.only(top=30)
        )

    def formulario_venta(self):
        self.producto_selector = ft.Dropdown(
            label="Seleccionar Producto",
            options=self.generar_lista_productos(),
            on_change=self.total_venta
        )
        self.cantidad_selector = ft.Dropdown(
            label="Seleccionar Cantidad",
            options=[ft.dropdown.Option(str(i)) for i in range(1, 11)],
            value="1",
            on_change=self.calcular_total  # Actualizar total al cambiar cantidad
        )
        self.total_parcial_text = ft.Text("Total Venta: CLP $0")
        agregar_venta_btn = ft.ElevatedButton("Agregar a la lista", on_click=self.agregar_a_lista, bgcolor=ft.Colors.BLUE_ACCENT,  color=ft.Colors.BLACK)
        return ft.Container(
            content=ft.Column([
                self.producto_selector,
                self.cantidad_selector,
                self.total_parcial_text,
                agregar_venta_btn
            ]),
        )

    def crear_lista_ventas(self):
        self.lista_ventas_container = ft.Column()
        return ft.Container(
            content=self.lista_ventas_container,
            padding=ft.padding.only(top=10)
        )

    def agregar_a_lista(self, e):
        producto_info = self.producto_selector.value
        if not producto_info:
            self.mostrar_mensaje("Por favor seleccione un producto.")
            return

        nombre_producto = producto_info.split(" (")[0]
        cantidad = int(self.cantidad_selector.value)
        producto = self.tienda.productos.obtener_item("Lapices", nombre_producto) or \
                    self.tienda.productos.obtener_item("Cuadernos", nombre_producto) or \
                    self.tienda.productos.obtener_item("Varios", nombre_producto)

        if producto:
            # Verificar si el producto ya está en la lista
            for item in self.lista_ventas:
                if item['producto'].nombre == nombre_producto:
                    item['cantidad'] += cantidad
                    self.mostrar_mensaje(f"Cantidad de '{nombre_producto}' actualizada.")
                    self.actualizar_lista_ventas()
                    self.total_venta()
                    return

            # Agregar nuevo producto a la lista
            self.lista_ventas.append({'producto': producto, 'cantidad': cantidad})
            self.actualizar_lista_ventas()
            self.total_venta()

    def actualizar_lista_ventas(self):
        self.lista_ventas_container.controls.clear()
        for item in self.lista_ventas:
            producto = item['producto']
            cantidad = item['cantidad']
            eliminar_btn = ft.IconButton(icon=ft.icons.REMOVE, on_click=lambda e, p=producto: self.eliminar_producto_lista(p))
            self.lista_ventas_container.controls.append(ft.Row([
                ft.Text(f"{producto.nombre} x{cantidad} - CLP ${producto.precio * cantidad:,.0f}"),
                eliminar_btn
            ]))
        self.lista_ventas_container.update()

    def eliminar_producto_lista(self, producto):
        self.lista_ventas = [item for item in self.lista_ventas if item['producto'] != producto]
        self.mostrar_mensaje(f"'{producto.nombre}' eliminado de la lista.")
        self.actualizar_lista_ventas()
        self.total_venta()

    def boton_finalizar_venta(self):
        return ft.ElevatedButton("Finalizar Venta", on_click=self.finalizar_venta)
    
    def total_venta(self):
        total = sum(item['producto'].precio * item['cantidad'] for item in self.lista_ventas)
        self.total_parcial_text.value = f"Total Venta: CLP ${total:,.0f}"
        self.total_parcial_text.update()
        return total

    def finalizar_venta(self, e):
        if not self.lista_ventas:
            self.mostrar_mensaje("No hay productos en la lista para finalizar la venta.")
            return

        total = sum(item['producto'].precio * item['cantidad'] for item in self.lista_ventas)
            
        # Cambiar el formato de fecha y hora
        fecha_hora = datetime.datetime.now()
        fecha_formateada = fecha_hora.strftime('%d-%m-%Y')  # Cambiar '/' por '-'
        hora_formateada = fecha_hora.strftime('%H-%M-%S')   # Mantener '-' en la hora
        
        # Generar voucher en PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Courier", size=12)
        pdf.cell(200, 10, txt=f"BOLETA EXENTA ELECTRONICA", ln=True, align='C')
        # Imprimir "Fecha:" y el dato de la fecha en la misma línea
        pdf.cell(100, 10, txt="Fecha:", ln=False)  # Ancho para "Fecha:"
        pdf.cell(0, 10, txt=fecha_hora.strftime('%d/%m/%Y'), ln=True, align='R')  # Alinear solo el dato a la derecha
        # Imprimir "Hora:" y el dato de la hora en la misma línea
        pdf.cell(100, 10, txt="Hora:", ln=False)  # Ancho para "Hora:"
        pdf.cell(0, 10, txt=hora_formateada, ln=True, align='R')  # Alinear solo el dato a la derecha        
        pdf.cell(100, 10, txt=f"Productos Vendidos:", ln=False)
        for item in self.lista_ventas:
            producto = item['producto']
            cantidad = item['cantidad']
            pdf.cell(0, 10, txt=f"{producto.nombre} x{cantidad}: CLP ${producto.precio * cantidad:,.0f}", ln=True, align='R')
        pdf.cell(200, 10, txt=f" ", ln=True, align='C')
        pdf.cell(100, 10, txt=f"Total: ", ln=False)
        pdf.cell(0, 10, txt=f"CLP ${total:,.0f}", ln=True, align='R')

        # Generar número de venta
        numero_venta = f"{self.contador_ventas:03d}"  # Formato 001, 002, etc.
        self.contador_ventas += 1  # Incrementar contador
        self.guardar_contador_ventas()  # Guardar el nuevo contador

        # Agregar número de venta al PDF
        pdf.cell(100, 10, txt=f"Número de Venta: ", ln=False)
        pdf.cell(0, 10, txt=numero_venta, ln=True, align='R')

        pdf.output(f"boleta_{fecha_formateada}_{hora_formateada}.pdf")

        # Guardar en ventas diarias
        self.ventas_diarias.append({
            "numero_venta": numero_venta,  # Agregar el número de venta aquí
            "productos": [f"{item['producto'].nombre} x{item['cantidad']}" for item in self.lista_ventas],
            "total": total,
            "fecha": fecha_formateada,
            "Hora": hora_formateada
            
        })
        
        # Limpiar la lista de ventas
        self.lista_ventas.clear()
        self.actualizar_lista_ventas()
        # Borrar el total del text
        self.total_parcial_text.value = "Total: CLP $0"
        self.total_parcial_text.update()
        
        self.mostrar_mensaje("Venta finalizada. Boleta generada.")

    def generar_lista_productos(self):
        return [
            ft.dropdown.Option(f"{item.nombre} ({item.tipo}) - CLP ${item.precio:,.0f}")
            for sublist in [self.tienda.productos.lapices, self.tienda.productos.cuadernos, self.tienda.productos.varios]
            for item in sublist
        ]
    
    #listaa
    def actualizar_lista_productos(self):
        self.producto_selector.options = self.generar_lista_productos()
        self.producto_selector_editar.options = self.generar_lista_productos()
        self.producto_selector_admin.options = self.generar_lista_productos()
        self.producto_selector.update()
        self.producto_selector_editar.update()
        self.producto_selector_admin.update()

    def actualizar_precio(self, e):
        producto_info = e.control.value
        nombre_producto = producto_info.split(" (")[0]
        self.producto_seleccionado = self.tienda.productos.obtener_item("Lapices", nombre_producto) or \
                                        self.tienda.productos.obtener_item("Cuadernos", nombre_producto) or \
                                        self.tienda.productos.obtener_item("Varios", nombre_producto)
        self.calcular_total()

    def calcular_total(self, e=None):
            if self.producto_seleccionado:
                self.cantidad = int(self.cantidad_selector.value)
                self.total_parcial = self.producto_seleccionado.precio * self.cantidad
                self.total_parcial_text.value = f"Total: CLP ${self.total_parcial:,.0f}"
                self.total_parcial_text.update()

    def guardar_ventas_en_excel(self, e=None):
        if not self.ventas_diarias:
            self.mostrar_mensaje("No hay ventas para guardar.")
            return
        
        df = pd.DataFrame(self.ventas_diarias)
        fecha = datetime.datetime.now()
        fecha_formateada = fecha.strftime('%d-%m-%Y') 
        archivo_excel = f"ventas_diarias_{fecha_formateada}.xlsx"
        df.to_excel(archivo_excel, index=False)

        # Reiniciar el contador de ventas a 1
        self.contador_ventas = 1
        self.guardar_contador_ventas()  # Guardar el contador reiniciado

    def agregar_tipo_producto(self, e):
        nuevo_tipo = self.nuevo_tipo_input.value
        if nuevo_tipo and nuevo_tipo not in self.tipos_productos:
            self.tipos_productos.append(nuevo_tipo)  # Agregar nuevo tipo a la lista
            self.mostrar_mensaje(f"Tipo de producto '{nuevo_tipo}' agregado exitosamente.")
            self.nuevo_tipo_input.value = ""
            self.guardar_tipos_productos()  # Guardar tipos de productos
            self.actualizar_lista_tipos()
            self.page.update()
        else:
            self.mostrar_mensaje("Por favor ingrese un tipo de producto válido o que no exista.")

    def eliminar_tipo_producto(self, e):
        tipo_a_eliminar = self.tipo_selector_eliminar.value
        if tipo_a_eliminar in self.tipos_productos:
            self.tipos_productos.remove(tipo_a_eliminar)  # Eliminar tipo de la lista
            self.mostrar_mensaje(f"Tipo de producto '{tipo_a_eliminar}' eliminado exitosamente.")
            self.guardar_tipos_productos()  # Guardar tipos de productos
            self.actualizar_lista_tipos()
            self.page.update()
        else:
            self.mostrar_mensaje("Por favor seleccione un tipo de producto válido para eliminar.")

    def generar_lista_tipos(self):
        return [ft.dropdown.Option(tipo) for tipo in self.tipos_productos]  # Devolver la lista actualizada

    def actualizar_lista_tipos(self):
        self.tipo_selector_eliminar.options = self.generar_lista_tipos()
        self.tipo_input_editar.options = self.generar_lista_tipos()
        self.tipo_input.options = self.generar_lista_tipos()
        self.tipo_input_editar.update()
        self.tipo_input.update()
        self.tipo_selector_eliminar.update()

    def cargar_tipos_productos(self):
        if os.path.exists("tipos_productos.json"):
            with open("tipos_productos.json", "r", encoding="UTF-8") as archivo:
                self.tipos_productos = json.load(archivo)
        else:
            # Si no existe el archivo, inicializar con tipos predeterminados
            self.tipos_productos = ["Lapices", "Cuadernos", "Varios"]

    def guardar_tipos_productos(self):
        with open("tipos_productos.json", "w", encoding="UTF-8") as archivo:
            json.dump(self.tipos_productos, archivo)

    def cargar_contador_ventas(self):
        if os.path.exists("contador_ventas.txt"):
            with open("contador_ventas.txt", "r") as archivo:
                return int(archivo.read().strip())
        return 1  # Iniciar en 1 si no existe el archivo

    def guardar_contador_ventas(self):
        with open("contador_ventas.txt", "w") as archivo:
            archivo.write(str(self.contador_ventas))

def main():
    app = TiendaGUI()
    ft.app(target=app.main)

if __name__ == "__main__":
    main()