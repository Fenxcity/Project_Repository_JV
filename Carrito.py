from Objetos import *
from Producto import *
class Carrito:
    def __init__(self, id_carrito):
        self.id_carrito = id_carrito
        self.productos = []
        self.quantity =[]
    def agregar_producto(self, producto, quantity):
        if producto.venta_producto(quantity):
            self.productos.append(producto)
            self.quantity.append(quantity)
        else: 
            print('No se pudo completar la transacción')

    def eliminar_producto(self, producto, quantity):
        self.productos.remove(producto)
        producto.re_stock(quantity)

    def mostrar_info_carrito(self):
        if len(self.productos) == 0:
            print('El carrito', self.id_carrito, 'esta vació')
        else:
            for producto in self.productos:
                print(producto.name, '$',producto.price)
    def clear_car(self):
        for producto in self.productos:
            producto.re_stock(self.quantity)
        self.productos.clear()

Car1 = Carrito(10001)

Car1.agregar_producto(Pepsi, 20)
Car1.mostrar_info_carrito()

Car1.clear_car()
Car1.mostrar_info_carrito()

Pepsi.consultar()
