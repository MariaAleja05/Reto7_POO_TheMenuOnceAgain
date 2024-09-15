class Producto:
    def __init__(self, nombre, precio):
        # Initialize a product with a name and price
        self.nombre = nombre
        self.precio = precio

    def __str__(self):
        # Return a string representation of the product
        return str(self.nombre) + str(" :") + str(self.precio)


class Menu:
    def __init__(self):
        # Initialize an empty list to hold the products in the menu
        self.productos = []

    def agregar_producto(self, producto):
        # Add a product to the menu
        self.productos.append(producto)

    def mostrar_menu(self):
        # Display the menu with the list of products
        print("\n--- Menu ---")
        for idx, producto in enumerate(self.productos, 1):
            print(str(idx) + str(producto))

    def obtener_producto(self, numero):
        # Get a product from the menu by its number
        if 1 <= numero <= len(self.productos):
            return self.productos[numero - 1]
        else:
            return None


class Pedido:
    def __init__(self):
        # Initialize an empty list to hold the items in the order
        self.items = []

    def agregar_item(self, producto, cantidad):
        # Add a product and its quantity to the order
        self.items.append((producto, cantidad))

    def mostrar_recibo(self):
        # Print the receipt of the order with totals
        print("\n--- Receipt ---")
        total = 0
        for producto, cantidad in self.items:
            subtotal = producto.precio * cantidad
            print(f'{producto.nombre} x {cantidad} = ${subtotal}')
            total += subtotal
        print(str("\nTotal to pay: $") + str(total))
        return total

    def __iter__(self):
        # Return an iterator for the order
        return PedidoIterable(self.items)


class PedidoIterable:
    """Implements an iterator for all items in the order"""

    def __init__(self, items):
        # Initialize the iterator with the order items
        self.items = items
        self.indice = 0

    def __iter__(self):
        # Return the iterator object itself
        return self

    def __next__(self):
        # Return the next item in the order or raise StopIteration if done
        if self.indice < len(self.items):
            item = self.items[self.indice]
            self.indice += 1
            return item
        else:
            raise StopIteration


class MedioPago:
    def __init__(self):
        pass

    def pagar(self, monto):
        # Abstract method to pay the amount, to be implemented by subclasses
        pass


class Tarjeta(MedioPago):
    def __init__(self, numero, cvv):
        super().__init__()
        # Initialize with card number and CVV
        self.numero = numero
        self.cvv = cvv

    def pagar(self, monto):
        # Print payment confirmation with card number (last 4 digits)
        print(str("Paying $ ") + str(monto) + str(" with card: ") + str(self.numero[-4:]))


class Efectivo(MedioPago):
    def __init__(self, monto_entregado):
        super().__init__()
        # Initialize with the amount of cash provided
        self.monto_entregado = monto_entregado

    def pagar(self, monto):
        # Handle payment with cash and provide change or insufficient funds message
        if self.monto_entregado >= monto:
            print(str("Payment made in cash. Change: $") + str(self.monto_entregado - monto))
        else:
            print(str("Insufficient funds. $") + str(monto - self.monto_entregado) + str(" needed to complete the payment."))


class Restaurante:
    def __init__(self):
        # Initialize the restaurant with a menu and an order
        self.menu = Menu()
        self.pedido = Pedido()

    def agregar_productos_menu(self):
        # Add products to the menu
        self.menu.agregar_producto(Producto('Combo hamburguesa', 30000))
        self.menu.agregar_producto(Producto('Ensalada Mexicana', 26000))
        self.menu.agregar_producto(Producto('Pizza personal toscana 6 quesos', 26000))
        self.menu.agregar_producto(Producto('Papas', 7000))
        self.menu.agregar_producto(Producto('Malteada', 17000))
        self.menu.agregar_producto(Producto('Gaseosa personal', 7000))
        self.menu.agregar_producto(Producto('Agua', 6000))
        self.menu.agregar_producto(Producto('Cerveza', 8000))

    def realizar_pedido(self):
        # Process a new order by allowing the user to select products and quantities
        while True:
            self.menu.mostrar_menu()
            opcion = int(input("Select the product number (0 to finish): "))
            if opcion == 0:
                break
            producto = self.menu.obtener_producto(opcion)
            if producto:
                cantidad = int(input(str("How many ") + str(producto.nombre) + str(" do you want?: ")))
                self.pedido.agregar_item(producto, cantidad)
            else:
                print("Invalid option, please try again.")

    def mostrar_recibo(self):
        # Display the receipt for the order
        return self.pedido.mostrar_recibo()

    def seleccionar_medio_pago(self, total):
        # Allow the user to select a payment method and process the payment
        print("\n--- Select payment method ---")
        print("1. Card")
        print("2. Cash")
        opcion = int(input("Option: "))

        if opcion == 1:
            numero = input("Enter the card number: ")
            cvv = input("Enter the CVV: ")
            tarjeta = Tarjeta(numero, cvv)
            tarjeta.pagar(total)
        elif opcion == 2:
            monto_entregado = float(input("Enter the amount of cash provided: "))
            efectivo = Efectivo(monto_entregado)
            efectivo.pagar(total)
        else:
            print("Invalid option.")


if __name__ == '__main__':
    # Main execution block
    restaurante = Restaurante()
    restaurante.agregar_productos_menu()
    restaurante.realizar_pedido()
    total = restaurante.mostrar_recibo()
    restaurante.seleccionar_medio_pago(total)

    print("\n--- Iterating over the order items ---")
    for producto, cantidad in restaurante.pedido:
        print(str(producto.nombre) + str(" x ") + str(cantidad))
