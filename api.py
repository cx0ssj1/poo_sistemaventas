from flask import Flask, request, jsonify
from flask_cors import CORS
from tienda import Tienda  # Importa tu lógica existente

app = Flask(__name__)
CORS(app)  # Permitir conexiones externas

# Instancia de la tienda
tienda = Tienda()

productos = [
    {"nombre": "Producto 1", "codigo": "QR123", "precio": 1000},
    {"nombre": "Producto 2", "codigo": "QR456", "precio": 2000},
]

@app.route('/api/buscar_producto', methods=['POST'])
def buscar_producto():
    data = request.json
    print(f"Datos recibidos: {data}")  # Muestra el contenido recibido
    codigo = data.get('codigo')

    if not codigo:
        return jsonify({'error': 'Código no proporcionado'}), 400

    # Simula la búsqueda del producto
    if codigo == "QR123":
        return jsonify({'nombre': 'Producto de prueba', 'precio': 1000, 'codigo': 'QR123'}), 200

    return jsonify({'error': 'Producto no encontrado'}), 404

if __name__ == '__main__':
    # Ejecuta el servidor Flask
    app.run(host='https://poo-sistemaventas.onrender.com', port=8080, debug=True)
