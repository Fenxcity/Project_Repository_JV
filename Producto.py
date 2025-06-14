class Producto:
    def __init__(self, id_code, name, price, brand, category, stock):
        self.id_code = id_code
        self.name = name
        self.price = price
        self.brand = brand
        self.category = category
        self.stock = stock
        self.status = 'Activo'
    def consultar(self):
        print('Información del producto', self.name)
        print('El precio del producto es: $', self.price, ', su código de producto es:', self.id_code, ', hay', self.stock, 'en existencia.')
    def venta_producto(self, quantity):
        if quantity > self.stock or self.stock <= 0:
            print('Inventario insuficiente, hay', self.stock, 'unidades en existencia.')
        else:    
            if quantity <= 0:
                print('Error, ingresar una cantidad valida.')
            else:
                self.stock -= quantity
                return True

    def re_stock(self, quantity):
        if quantity <= 0:
            print('Ingrese una cantidad válida')
        else:
            self.stock +=  quantity
            print('El nuevo inventario es:', self.stock, 'unidades de', self.name)

    def modificar_precio(self, modification):
        self.price += (self.price * modification) / 100
        if modification >= 0:
            print('El producto subió', modification, '%')
            print('Por lo tanto el nuevo precio es:', self.price)
        else:
            print('El producto bajó', modification, '%')
            print('Por lo tanto el nuevo precio es:', self.price)

    def change_status(self, nuevo_estado):
        nuevo_estado = nuevo_estado.lower()
        nuevo_estadoc = ''
        for letra in nuevo_estado:
            if letra != ' ':
                nuevo_estadoc = nuevo_estadoc + letra
        if nuevo_estadoc != 'agotado' and nuevo_estadoc != 'caducado' and nuevo_estadoc != 'perecedero' and nuevo_estadoc != 'activo':
            print('Error, ingrese un valor válido')
        else:
            if nuevo_estado == 'agotado':
                self.status = 'Agotado'
            elif nuevo_estado == 'caducado':
                self.status = 'Caducado'
            elif nuevo_estado == 'perecedero':
                self.status = 'Perecedero'
            elif nuevo_estadoc == 'activo':
                self.status = 'Activo'

    

class Bebidas(Producto):
    def shakear(self, mezclador):
        pass
