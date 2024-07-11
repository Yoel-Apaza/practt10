import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import json
import streamlit as st

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
        st.plotly_chart(fig)

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
def main():
    st.title("Visualización de Superficies 3D")

    tipo_superficie = st.selectbox("Seleccione el tipo de superficie:",
                                   ("Plano", "Paraboloide", "Sinusoide", "Hiperboloide"))
    parametro = st.slider("Ajustar parámetro:", min_value=-5.0, max_value=5.0, value=1.0, step=0.1)

    if st.button("Visualizar"):
        if tipo_superficie == "Plano":
            superficie = Plano((-5, 5), (-5, 5), parametro)
        elif tipo_superficie == "Paraboloide":
            superficie = Paraboloide((-5, 5), (-5, 5), parametro)
        elif tipo_superficie == "Sinusoide":
            superficie = Sinusoide((-5, 5), (-5, 5), parametro)
        elif tipo_superficie == "Hiperboloide":
            superficie = Hiperboloide((-5, 5), (-5, 5), parametro)
        else:
            st.error("Opción no válida.")
            return

        visualizador = Visualizador3DPlotly(superficie)
        visualizador.mostrar_con_plotly()

    if st.button("Guardar Configuración"):
        if tipo_superficie == "Plano":
            superficie = Plano((-5, 5), (-5, 5), parametro)
        elif tipo_superficie == "Paraboloide":
            superficie = Paraboloide((-5, 5), (-5, 5), parametro)
        elif tipo_superficie == "Sinusoide":
            superficie = Sinusoide((-5, 5), (-5, 5), parametro)
        elif tipo_superficie == "Hiperboloide":
            superficie = Hiperboloide((-5, 5), (-5, 5), parametro)
        else:
            st.error("Opción no válida.")
            return

        guardar_configuracion(superficie)
        st.success("Configuración guardada")

    if st.button("Cargar Configuración"):
        try:
            superficie = cargar_configuracion()
            st.write(f"Superficie cargada: {superficie.__class__.__name__}")
            st.write(f"Parámetro: {superficie.parametro}")
        except Exception as e:
            st.error(f"Error al cargar configuración: {e}")

if __name__ == "__main__":
    main()
