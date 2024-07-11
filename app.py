import streamlit as st
import visualizacion_3d

def main():
    st.title('Visualización de Superficies 3D')

    tipo_superficie = st.selectbox("Seleccione el tipo de superficie:",
                                   ("Plano", "Paraboloide", "Sinusoide", "Hiperboloide"))

    parametro = st.slider("Ajustar parámetro:", min_value=-5.0, max_value=5.0, value=1.0, step=0.1)

    if st.button("Mostrar superficie"):
        if tipo_superficie == "Plano":
            superficie = visualizacion_3d.Plano((-5, 5), (-5, 5), parametro)
        elif tipo_superficie == "Paraboloide":
            superficie = visualizacion_3d.Paraboloide((-5, 5), (-5, 5), parametro)
        elif tipo_superficie == "Sinusoide":
            superficie = visualizacion_3d.Sinusoide((-5, 5), (-5, 5), parametro)
        elif tipo_superficie == "Hiperboloide":
            superficie = visualizacion_3d.Hiperboloide((-5, 5), (-5, 5), parametro)
        else:
            st.error("Opción no válida.")

        visualizador = visualizacion_3d.Visualizador3DPlotly(superficie)
        visualizador.mostrar_con_plotly()

if __name__ == "__main__":
    main()
