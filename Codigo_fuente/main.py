# main.py (arranque de todo)

# Importación de la librería base para interfaces gráficas
import tkinter as tk
# Importación de la clase WifiApp que contiene la lógica visual y funcional
from gui import WifiApp

def main():
    # Inicialización de la ventana raíz de la aplicación
    root = tk.Tk()
    # Instanciación de la aplicación pasando la ventana raíz como contenedor
    app = WifiApp(root)
    # Ejecución del bucle principal para mantener la ventana abierta y procesar eventos
    root.mainloop()

# Punto de entrada estándar de Python para ejecutar el script
if __name__ == "__main__":
    main()
