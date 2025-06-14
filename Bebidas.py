from Producto import Producto

class Bebidas(Producto):
    def __init__(self, id_code, name, price, brand, category, stock, tipo):
        super().__init__(id_code, name, price, brand, category, stock)
        self.tipo = tipo
    
