import qrcode
import os

# Lista de productos con sus códigos únicos
productos = [
    {"nombre": "Producto 1", "codigo": "QR123"},
    {"nombre": "Producto 2", "codigo": "QR456"},
    {"nombre": "Producto 3", "codigo": "QR789"},
]

# Carpeta para guardar los códigos QR
output_folder = "codigos_qr"
os.makedirs(output_folder, exist_ok=True)

# Generar QR para cada producto
for producto in productos:
    codigo = producto["codigo"]
    nombre = producto["nombre"]
    
    # Crear el QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=4,
    )
    qr.add_data(codigo)
    qr.make(fit=True)
    
    # Guardar la imagen del QR
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(os.path.join(output_folder, f"{nombre}.png"))

print(f"Códigos QR generados en la carpeta: {output_folder}")
