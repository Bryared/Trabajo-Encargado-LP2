# --------------------------------------------------------------------------
# SCRIPT 2: VISUALIZADOR DE RENDIMIENTO DE ACCIONES
# --------------------------------------------------------------------------
#
# OBJETIVO:
# Este script lee los archivos CSV de datos de acciones, calcula el
# rendimiento porcentual normalizado de cada activo y crea un gráfico
# interactivo para comparar su evolución en el tiempo.
#
# PRERREQUISITOS:
# 1. Haber ejecutado primero el script 'extractor_acciones.py'.
# 2. Tener instaladas las librerías necesarias.
#    Abre tu terminal y ejecuta:
#    pip install pandas plotly nbformat
#
# --------------------------------------------------------------------------

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import os

# --- CORRECCIÓN DE RENDERIZADO ---
# Establece el renderizador por defecto para evitar errores con 'nbformat'.
pio.renderers.default = 'browser'

# --- CONFIGURACIÓN PRINCIPAL ---

# 1. Lista de símbolos de acciones que queremos comparar en el gráfico.
#    Deben coincidir con los nombres de los archivos CSV generados.
ACTIVOS_A_COMPARAR = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'SPY']

# 2. Carpeta donde se encuentran los archivos CSV de las acciones.
CARPETA_DATOS_CSV = 'grupo1/ACTIVOS_GUIA/datos_acciones_csv'
# 3. Moneda base para identificar la columna de precios.
MONEDA_COTIZACION = 'usd'


def cargar_y_normalizar_datos_acciones(lista_activos):
    """
    Carga los datos de acciones desde los archivos CSV, los normaliza para
    comparar rendimientos y los une en un solo DataFrame.

    Args:
        lista_activos (list): Una lista con los símbolos de los activos a cargar.

    Returns:
        pandas.DataFrame: Un DataFrame con las fechas como índice y una
                          columna por cada activo con su rendimiento normalizado.
    """
    print("--- Cargando y Normalizando Datos de Acciones ---")
    df_comparativo = pd.DataFrame()
    columna_precio = f'precio_{MONEDA_COTIZACION}'

    for simbolo in lista_activos:
        ruta_archivo = os.path.join(CARPETA_DATOS_CSV, f"{simbolo}_datos_historicos.csv")

        if not os.path.exists(ruta_archivo):
            print(f"ADVERTENCIA: No se encontró el archivo para '{simbolo}'. Se omitirá.")
            continue

        df_activo = pd.read_csv(ruta_archivo, index_col=0, parse_dates=True)
        # Renombramos el índice a 'fecha' para consistencia
        df_activo.index.name = 'fecha'
        
        # Normalización del precio
        precio_inicial = df_activo[columna_precio].iloc[0]
        rendimiento_normalizado = ((df_activo[columna_precio] / precio_inicial) - 1) * 100
        
        df_comparativo[simbolo] = rendimiento_normalizado
        print(f"Datos de '{simbolo}' cargados y normalizados.")

    return df_comparativo


def generar_grafico_comparativo_acciones(df_datos):
    """
    Genera un gráfico de líneas interactivo usando Plotly para comparar acciones.

    Args:
        df_datos (pandas.DataFrame): DataFrame con los datos de rendimiento a graficar.
    """
    print("\n--- Generando Gráfico Interactivo de Acciones ---")
    fig = go.Figure()

    for activo in df_datos.columns:
        fig.add_trace(go.Scatter(
            x=df_datos.index,
            y=df_datos[activo],
            mode='lines',
            name=activo
        ))

    fig.update_layout(
        title='Rendimiento Porcentual Comparativo de Acciones',
        xaxis_title='Fecha',
        yaxis_title='Rendimiento Normalizado (%)',
        legend_title='Activos',
        template='plotly_dark',
        hovermode='x unified'
    )
    
    nombre_archivo_html = 'comparativa_rendimiento_acciones.html'
    fig.write_html(nombre_archivo_html)
    
    print(f"Gráfico guardado como '{nombre_archivo_html}'. Abriendo en el navegador...")
    fig.show()


# --- Punto de Entrada del Script ---
if __name__ == "__main__":
    datos_comparativos = cargar_y_normalizar_datos_acciones(ACTIVOS_A_COMPARAR)

    if not datos_comparativos.empty:
        generar_grafico_comparativo_acciones(datos_comparativos)
    else:
        print("\nNo se encontraron datos para graficar. Asegúrate de haber ejecutado primero 'extractor_acciones.py'.")
