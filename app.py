import flet as ft
from tienda import Tienda
from clientes import Cliente
from pedidos import Pedido
import datetime
import pandas as pd
from fpdf import FPDF

class TiendaGUI:
    def __init__(self):
        self.tienda = Tienda()
        self.producto_seleccionado = None
        self.cantidad = 1
        self.total_parcial = 0.0
        self.lista_productos = []
        self.ventas_diarias = [] 

    def main(self, page: ft.Page):
        page.title = "Sistema de Tienda Matilde"
        page.padding = 20
        page.theme_mode = "dark"
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Administración",
                    content=self.crear_vista_admin()
                ),
                ft.Tab(
                    text="Ventas",
                    content=self.crear_vista_ventas()
                ),
            ],
            expand=1,
        )
        page.add(self.tabs)
        self.page = page

    def mostrar_mensaje(self, mensaje):
        dialog = ft.AlertDialog(title=ft.Text(mensaje))
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def crear_vista_admin(self):
            guardar_ventas_btn = ft.ElevatedButton("Guardar Ventas Diarias en Excel", on_click=lambda _: self.guardar_ventas_en_excel())
            return ft.Container(
                content=ft.Column([
                    ft.Text("Administración del Local", size=20, weight=ft.FontWeight.BOLD),
                    self.formulario_producto(),
                    guardar_ventas_btn
                ])
            )
    def formulario_producto(self):
        self.nombre_input = ft.TextField(label="Nombre del Producto")
        self.precio_input = ft.TextField(label="Precio del Producto")
        self.tipo_input = ft.Dropdown(
            label="Tipo de Producto",
            options=[
                ft.dropdown.Option("Lapices"),
                ft.dropdown.Option("Cuadernos"),
                ft.dropdown.Option("Varios")
            ]
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
        # Actualizar la lista de productos en el área de ventas
        self.actualizar_lista_productos()
        self.page.update()

    def crear_vista_ventas(self):
        return ft.Container(
            content=ft.Column([
                ft.Text("Gestión de Ventas", size=20, weight=ft.FontWeight.BOLD),
                self.formulario_venta()
            ])
        )

    def formulario_venta(self):
        self.cliente_nombre_input = ft.TextField(label="Nombre del Cliente")
        self.producto_selector = ft.Dropdown(
            label="Seleccionar Producto",
            options=self.generar_lista_productos(),
            on_change=self.actualizar_precio
        )
        self.cantidad_selector = ft.Dropdown(
            label="Seleccionar Cantidad",
            options=[ft.dropdown.Option(str(i)) for i in range(1, 11)],
            value="1",
            on_change=self.calcular_total
        )
        self.total_parcial_text = ft.Text("Total parcial: CLP $0")
        finalizar_venta_btn = ft.ElevatedButton("Finalizar Venta", on_click=self.finalizar_venta)
        
        return ft.Column([
            self.cliente_nombre_input,
            self.producto_selector,
            self.cantidad_selector,
            self.total_parcial_text,
            finalizar_venta_btn
        ])

    def generar_lista_productos(self):
        return [
            ft.dropdown.Option(f"{item.nombre} ({item.tipo}) - CLP ${item.precio:,.0f}")
            for sublist in [self.tienda.productos.lapices, self.tienda.productos.cuadernos, self.tienda.productos.varios]
            for item in sublist
        ]

    def actualizar_lista_productos(self):
        self.producto_selector.options = self.generar_lista_productos()
        self.producto_selector.update()

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

    def guardar_ventas_en_excel(self):
            if not self.ventas_diarias:
                self.mostrar_mensaje("No hay ventas para guardar.")
                return
            df = pd.DataFrame(self.ventas_diarias)
            fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d')
            archivo_excel = f"ventas_diarias_{fecha_actual}.xlsx"
            df.to_excel(archivo_excel, index=False)
            self.mostrar_mensaje(f"Ventas guardadas exitosamente en {archivo_excel}.")

    def finalizar_venta(self, e):
        if not self.producto_seleccionado:
            self.mostrar_mensaje("Por favor seleccione un producto.")
            return
        
        cliente_nombre = self.cliente_nombre_input.value
        cantidad = self.cantidad
        total = self.total_parcial
        
        pedido = Pedido([self.producto_seleccionado])
        self.tienda.crear_pedido(Cliente(), pedido)
        
        self.ventas_diarias.append({
            "Producto": self.producto_seleccionado.nombre,
            "Cantidad": cantidad,
            "Total": total
        })
        
        # Generar voucher en PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Voucher de Venta", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Cliente: {cliente_nombre}", ln=True)
        pdf.cell(200, 10, txt=f"Producto: {self.producto_seleccionado.nombre}", ln=True)
        pdf.cell(200, 10, txt=f"Cantidad: {cantidad}", ln=True)
        pdf.cell(200, 10, txt=f"Precio Unitario: CLP ${self.producto_seleccionado.precio:,.0f}", ln=True)
        pdf.cell(200, 10, txt=f"Total: CLP ${total:,.0f}", ln=True)
        pdf.cell(200, 10, txt=f"Fecha y Hora: {datetime.datetime.now()}", ln=True)
        pdf.output(f"voucher_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
        
        # Registrar venta en Excel
        fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d')
        archivo_excel = f"ventas_{fecha_actual}.xlsx"
        
        try:
            datos_excel = pd.read_excel(archivo_excel)
        except FileNotFoundError:
            datos_excel = pd.DataFrame(columns=["Producto", "Cantidad", "Total"])
            
        nueva_fila = {"Producto": self.producto_seleccionado.nombre, "Cantidad": cantidad, "Total": total}
        datos_excel = datos_excel.append(nueva_fila, ignore_index=True)
        total_diario = datos_excel["Total"].sum()
        datos_excel.loc[len(datos_excel)] = {"Producto": "TOTAL DIARIO", "Cantidad": "-", "Total": total_diario}

        datos_excel.to_excel(archivo_excel, index=False)

        self.mostrar_mensaje(f"Venta finalizada. Voucher generado y guardado en {archivo_excel}.")


def main():
    app = TiendaGUI()
    ft.app(target=app.main)

if __name__ == "__main__":
    main()
