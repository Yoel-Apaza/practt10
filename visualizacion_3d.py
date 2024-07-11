import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import tkinter as tk
from tkinter import ttk
import json

# Clase base para las superficies 3D
class Superficie3D:
    def __init__(self, x_range, y_range):
        self.x_range = x_range
        self.y_range = y_range
        self.x, self.y = np.meshgrid(np.linspace(x_range[0], x_range[1], 100), 
                                     np.linspace(y_range[0], y_range[1], 100))

    def calcular_z(self):
        raise NotImplementedError("Este método debe ser implementado por las subclases")

    def generar_datos(self):
        self.z = self.calcular_z()
        return self.x, self.y, self.z

# Subclase para representar un plano
class Plano(Superficie3D):
    def __init__(self, x_range, y_range, pendiente):
        super().__init__(x_range, y_range)
        self.pendiente = pendiente

    def calcular_z(self):
        return self.pendiente * self.x

# Subclase para representar un paraboloide
class Paraboloide(Superficie3D):
    def __init__(self, x_range, y_range, coef):
        super().__init__(x_range, y_range)
        self.coef = coef

    def calcular_z(self):
        return self.coef * (self.x**2 + self.y**2)

# Subclase para representar una sinusoide
class Sinusoide(Superficie3D):
    def __init__(self, x_range, y_range, frecuencia):
        super().__init__(x_range, y_range)
        self.frecuencia = frecuencia

    def calcular_z(self):
        return np.sin(self.frecuencia * np.sqrt(self.x**2 + self.y**2))

# Subclase para representar un hiperboloide
class Hiperboloide(Superficie3D):
    def __init__(self, x_range, y_range, coef):
        super().__init__(x_range, y_range)
        self.coef = coef

    def calcular_z(self):
        return self.coef * (self.x**2 - self.y**2)

# Clase para visualizar superficies utilizando Matplotlib
class Visualizador3D:
    def __init__(self, superficie):
        self.superficie = superficie

    def mostrar_con_matplotlib(self):
        x, y, z = self.superficie.generar_datos()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(x, y, z, cmap='viridis')
        plt.show()

# Clase para visualizar superficies utilizando Plotly
class Visualizador3DPlotly(Visualizador3D):
    def mostrar_con_plotly(self):
        x, y, z = self.superficie.generar_datos()
        fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
        fig.update_layout(title='Superficie 3D', autosize=False, width=800, height=800)
        fig.show()

# Funciones para guardar y cargar configuraciones
def guardar_configuracion(superficie, filename="configuracion.json"):
    config = {
        "tipo": superficie.__class__.__name__,
        "x_range": superficie.x_range,
        "y_range": superficie.y_range,
        "parametro": getattr(superficie, superficie.parametro_nombre, None)
    }
    with open(filename, 'w') as f:
        json.dump(config, f)

def cargar_configuracion(filename="configuracion.json"):
    with open(filename, 'r') as f:
        config = json.load(f)

    tipo = config["tipo"]
    x_range = tuple(config["x_range"])
    y_range = tuple(config["y_range"])
    parametro = config["parametro"]

    if tipo == "Plano":
        return Plano(x_range, y_range, parametro)
    elif tipo == "Paraboloide":
        return Paraboloide(x_range, y_range, parametro)
    elif tipo == "Sinusoide":
        return Sinusoide(x_range, y_range, parametro)
    elif tipo == "Hiperboloide":
        return Hiperboloide(x_range, y_range, parametro)
    else:
        raise ValueError("Tipo de superficie no válido.")

# Interfaz gráfica para seleccionar y visualizar superficies
class AplicacionVisualizacion3D:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualización de Superficies 3D")
        self.crear_widgets()

    def crear_widgets(self):
        frame = ttk.Frame(self.root, padding="10 10 10 10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.tipo_superficie = tk.StringVar()
        self.parametro = tk.DoubleVar()

        ttk.Label(frame, text="Seleccione el tipo de superficie:").grid(row=0, column=0, columnspan=2)
        ttk.Radiobutton(frame, text="Plano", variable=self.tipo_superficie, value="Plano").grid(row=1, column=0, sticky=tk.W)
        ttk.Radiobutton(frame, text="Paraboloide", variable=self.tipo_superficie, value="Paraboloide").grid(row=2, column=0, sticky=tk.W)
        ttk.Radiobutton(frame, text="Sinusoide", variable=self.tipo_superficie, value="Sinusoide").grid(row=3, column=0, sticky=tk.W)
        ttk.Radiobutton(frame, text="Hiperboloide", variable=self.tipo_superficie, value="Hiperboloide").grid(row=4, column=0, sticky=tk.W)

        ttk.Label(frame, text="Ingrese el parámetro:").grid(row=5, column=0)
        ttk.Entry(frame, textvariable=self.parametro).grid(row=5, column=1)

        ttk.Button(frame, text="Visualizar", command=self.visualizar).grid(row=6, column=0, columnspan=2)
        ttk.Button(frame, text="Guardar Configuración", command=self.guardar).grid(row=7, column=0, columnspan=2)
        ttk.Button(frame, text="Cargar Configuración", command=self.cargar).grid(row=8, column=0, columnspan=2)

    def visualizar(self):
        tipo = self.tipo_superficie.get()
        parametro = self.parametro.get()

        if tipo == "Plano":
            superficie = Plano((-5, 5), (-5, 5), parametro)
        elif tipo == "Paraboloide":
            superficie = Paraboloide((-5, 5), (-5, 5), parametro)
        elif tipo == "Sinusoide":
            superficie = Sinusoide((-5, 5), (-5, 5), parametro)
        elif tipo == "Hiperboloide":
            superficie = Hiperboloide((-5, 5), (-5, 5), parametro)
        else:
            print("Opción no válida.")
            return

        visualizador = Visualizador3DPlotly(superficie)
        visualizador.mostrar_con_plotly()

    def guardar(self):
        tipo = self.tipo_superficie.get()
        parametro = self.parametro.get()

        if tipo == "Plano":
            superficie = Plano((-5, 5), (-5, 5), parametro)
        elif tipo == "Paraboloide":
            superficie = Paraboloide((-5, 5), (-5, 5), parametro)
        elif tipo == "Sinusoide":
            superficie = Sinusoide((-5, 5), (-5, 5), parametro)
        elif tipo == "Hiperboloide":
            superficie = Hiperboloide((-5, 5), (-5, 5), parametro)
        else:
            print("Opción no válida.")
            return

        guardar_configuracion(superficie)

    def cargar(self):
        try:
            superficie = cargar_configuracion()
            self.tipo_superficie.set(superficie.__class__.__name__)
            self.parametro.set(superficie.parametro)
        except Exception as e:
            print(f"Error al cargar configuración: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionVisualizacion3D(root)
    root.mainloop()
