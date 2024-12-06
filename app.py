import flet as ft
from tienda import Tienda
from clientes import Cliente

class TiendaGUI:
    def __init__(self):
        self.tienda = Tienda()
    def main(self, page: ft.Page):
        page.title = "sistema de Matilde Tienda"
        page.padding = 20
        page.theme_mode = "dark"
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Admin",
                    content=self.crear_vista_admin()
                ),
                ft.Tab(
                    text="Venta",
                    content=self.crear_vista_ventas()
                ),
            ],
            expand=1,
        )
        page.add(self.tabs)
    #metodos de vistas
    def crear_vista_admin(self):
        return ft.Container(
            content=ft.Text("Administracion Del Local", size=20, weight=ft.FontWeight.BOLD),
        )
    def crear_vista_ventas(self):
        return ft.Container(
            content=ft.Text("Venta", size=20, weight=ft.FontWeight.BOLD),
        )
    #metodos internos de vistas
def main():
    app = TiendaGUI()
    ft.app(target=app.main)
if __name__ == "__main__":
    main()