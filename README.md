# Visualización de Superficies 3D

Este proyecto permite visualizar y manipular superficies matemáticas en 3D utilizando Python y diversas bibliotecas gráficas.

## Funcionalidades

- Se pueden seleccionar diferentes tipos de superficies (Plano, Paraboloide, Sinusoide, Hiperboloide).
- Permite ajustar parámetros y ver cómo cambian las gráficas en tiempo real.
- Incluye una interfaz gráfica simple para la interacción del usuario.

## Mejoras Implementadas

- **Añadido soporte para el Hiperboloide**: Se implementó una nueva clase `Hiperboloide` que permite visualizar esta superficie.
- **Persistencia de configuraciones**: Se añadieron funciones para guardar y cargar configuraciones de superficies desde un archivo JSON.
- **Interfaz gráfica mejorada**: La interfaz gráfica ahora incluye botones para guardar y cargar configuraciones, facilitando la reutilización de visualizaciones.

## Ejecución del Proyecto

Para ejecutar el proyecto:

1. Asegúrate de tener instaladas las siguientes bibliotecas:
   - NumPy
   - Matplotlib
   - Plotly
   - Tkinter (normalmente incluido con Python estándar)

2. Ejecuta el archivo `visualizacion_3d.py`:
   ```bash
   python visualizacion_3d.py
