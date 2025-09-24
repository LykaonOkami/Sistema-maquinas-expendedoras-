
from datetime import datetime
import uuid
import time 
class Usuario:
    def __init__(self, id_usuario):
        self.id_usuario = id_usuario

class Producto:
    def __init__(self, id_producto, nombre, precio, stock):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = float(precio)
        self.stock = int(stock)

    def verificar_disponibilidad(self):
        return self.stock > 0

    def actualizar_stock(self):
        if self.stock > 0:
            self.stock -= 1

class Transaccion:
    def __init__(self, producto, monto, metodo_pago):
        self.id_transaccion = str(uuid.uuid4())
        self.producto = producto
        self.monto = monto
        self.metodo_pago = metodo_pago
        self.fecha_hora = datetime.now()
        self.estado = "aprobado"

class MaquinaExpendedora:
    def __init__(self, id_maquina, ubicacion, efectivo_inicial=100.0):
        self.id_maquina = id_maquina
        self.ubicacion = ubicacion
        self.productos = []
        self.historial_transacciones = []
        self.efectivo_disponible = float(efectivo_inicial)

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def mostrar_productos(self):
        print("\n" + "="*35)
        print("    PRODUCTOS DISPONIBLES")
        print("="*35)
        # Se enumeran los productos para selección
        for i, p in enumerate(self.productos):
            disponibilidad = "✅" if p.verificar_disponibilidad() else "❌ AGOTADO"
            print(f"  {i+1}. {p.nombre:<20} ${p.precio:>5.2f}  {disponibilidad}")
        print("="*35)

    def _procesar_pago_tarjeta(self, producto):
        print("\n💳 Procesando pago con tarjeta...")
        time.sleep(2) # Simula el tiempo de procesamiento
        print("Lectura de chip... Aprobando transacción...")
        time.sleep(2)
        return True # Simulación simple: el pago con tarjeta siempre es exitoso

    def _procesar_pago_efectivo(self, producto):
        print(f"\n💵 El costo es de ${producto.precio:.2f}. Por favor, ingrese el dinero.")
        while True:
            try:
                dinero_ingresado = float(input("Ingrese la cantidad: $"))
                if dinero_ingresado < producto.precio:
                    print(f"Dinero insuficiente. Faltan ${producto.precio - dinero_ingresado:.2f}")
                    continue
                
                cambio = dinero_ingresado - producto.precio
                if cambio > self.efectivo_disponible:
                    print("Lo sentimos, la máquina no tiene suficiente cambio. Intente con otro método o un monto exacto.")
                    return False

                if cambio > 0:
                    print(f"Su cambio es de: ${cambio:.2f}")

                # Actualizamos el efectivo de la máquina
                self.efectivo_disponible += producto.precio
                return True

            except ValueError:
                print("Por favor, ingrese una cantidad numérica válida.")

    def iniciar_compra(self):
        try:
            opcion = int(input("\nSeleccione el número del producto que desea comprar: "))
            # Verificamos que el producto exista en la lista
            if 1 <= opcion <= len(self.productos):
                producto_elegido = self.productos[opcion-1]
            else:
                print("❌ Opción inválida. Ese producto no existe.")
                return

        except ValueError:
            print("❌ Error: debe ingresar un número.")
            return

        if not producto_elegido.verificar_disponibilidad():
            print(f"Lo sentimos, el producto '{producto_elegido.nombre}' está agotado.")
            return
        
        # Selección de método de pago
        metodo_pago = input("¿Cómo desea pagar? (tarjeta / efectivo): ").lower()
        
        pago_exitoso = False
        if metodo_pago == "tarjeta":
            pago_exitoso = self._procesar_pago_tarjeta(producto_elegido)
        elif metodo_pago == "efectivo":
            pago_exitoso = self._procesar_pago_efectivo(producto_elegido)
        else:
            print("Método de pago no reconocido.")
            return

        if pago_exitoso:
            producto_elegido.actualizar_stock()
            nueva_transaccion = Transaccion(producto_elegido, producto_elegido.precio, metodo_pago)
            self.historial_transacciones.append(nueva_transaccion)
            print("\n" + "*"*30)
            print("✅ ¡Pago exitoso!")
            print(f"Dispensando: {producto_elegido.nombre}")
            print("¡Gracias por su compra!")
            print("*"*30)
            time.sleep(2)


# --- LÓGICA PRINCIPAL (MOTOR INTERACTIVO) ---

def main():
    # 1. Configuración inicial
    mi_maquina = MaquinaExpendedora(id_maquina="ME-JURIQUILLA-01", ubicacion="Entrada principal")
    mi_maquina.agregar_producto(Producto(1, "Agua Embotellada", 12.00, 10))
    mi_maquina.agregar_producto(Producto(2, "Jugo de Naranja", 15.50, 8))
    mi_maquina.agregar_producto(Producto(3, "Papas de Sal", 18.00, 5))
    mi_maquina.agregar_producto(Producto(4, "Barra de Cereal", 22.00, 0))
    mi_maquina.agregar_producto(Producto(5, "Café Frío", 35.00, 4))
    
    print("👋 ¡Bienvenido a la Máquina Expendedora!")

    # 2. Bucle principal de la aplicación
    while True:
        print("\n-- MENÚ PRINCIPAL --")
        print("1. Ver productos")
        print("2. Comprar un producto")
        print("3. Salir")
        
        opcion_menu = input("¿Qué desea hacer?: ")
        
        if opcion_menu == "1":
            mi_maquina.mostrar_productos()
        elif opcion_menu == "2":
            mi_maquina.mostrar_productos() # Mostramos productos antes de que elija
            mi_maquina.iniciar_compra()
        elif opcion_menu == "3":
            print("\nGracias por usar la máquina. ¡Hasta pronto! 👋")
            break
        else:
            print("\nOpción no válida. Por favor, elija 1, 2 o 3.")

# Esto asegura que la función main() se ejecute al correr el script
if __name__ == "__main__":
    main()