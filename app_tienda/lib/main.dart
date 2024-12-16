import 'package:flutter/material.dart';
import 'package:barcode_scan2/barcode_scan2.dart'; // Agrega esta dependencia en pubspec.yaml
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'App Tienda',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Sistema de Ventas'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  List<Map<String, dynamic>> _productos = []; // Lista de productos escaneados
  double _total = 0.0; // Total acumulado

  // Escanear un producto usando código de barras o QR
  Future<void> escanearProducto() async {
    try {
      var result = await BarcodeScanner.scan();
      if (result.rawContent.isNotEmpty) {
        // Llama al backend para buscar el producto
        final response = await http.post(
          Uri.parse('http://192.168.1.7:8080/api/buscar_producto'), // Reemplaza <TU_IP> con la IP de tu servidor
          body: jsonEncode({'codigo': result.rawContent}),
          headers: {'Content-Type': 'application/json'},
        );

        if (response.statusCode == 200) {
          final producto = jsonDecode(response.body);
          setState(() {
            _productos.add(producto);
            _total += producto['precio'];
          });
        } else {
          mostrarMensaje('Producto no encontrado.');
        }
      }
    } catch (e) {
      mostrarMensaje('Error al escanear: $e');
    }
  }

  // Mostrar mensajes en pantalla
  void mostrarMensaje(String mensaje) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(mensaje)));
  }

  // Finalizar la venta
  void finalizarVenta() {
    setState(() {
      _productos.clear();
      _total = 0.0;
    });
    mostrarMensaje('Venta finalizada.');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Column(
        children: [
          ElevatedButton(
            onPressed: escanearProducto,
            child: const Text('Escanear Producto'),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: _productos.length,
              itemBuilder: (context, index) {
                final producto = _productos[index];
                return ListTile(
                  title: Text(producto['nombre']),
                  subtitle: Text('Precio: \$${producto['precio']}'),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Text(
              'Total: \$$_total',
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
          ),
          ElevatedButton(
            onPressed: finalizarVenta,
            child: const Text('Finalizar Venta'),
          ),
        ],
      ),
    );
  }
}
