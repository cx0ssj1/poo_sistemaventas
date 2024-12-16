from flask import Flask, request, jsonify
from flask_cors import CORS
from tienda import Tienda  # Importa tu lógica existente

app = Flask(__name__)
CORS(app)  # Permitir conexiones externas

# Instancia de la tienda
tienda = Tienda()

@app.route('/api/buscar_producto', methods=['POST'])
def buscar_producto():
    """Buscar un producto por su código"""
    data = request.json
    codigo = data.get('codigo')  # Código enviado desde la app
    producto = tienda.productos.buscar_por_codigo(codigo)  # Usa tu lógica
    if producto:
        return jsonify({
            'nombre': producto.nombre,
            'precio': producto.precio,
            'codigo': producto.codigo,
        }), 200
    return jsonify({'error': 'Producto no encontrado'}), 404

if __name__ == '__main__':
    # Ejecuta el servidor Flask
    app.run(host='0.0.0.0', port=8080, debug=True)
