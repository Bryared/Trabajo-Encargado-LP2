# --------------------------------------------------------------------------
# FASE 3: VISUALIZADOR DE RENDIMIENTO DE CRIPTOMONEDAS (Corregido)
# --------------------------------------------------------------------------
#
# OBJETIVO:
# Este script lee los archivos CSV generados previamente, calcula el
# rendimiento porcentual normalizado de cada activo y crea un gráfico
# interactivo para comparar su evolución en el tiempo.
#
# PRERREQUISITOS:
# 1. Haber ejecutado primero el script 'extractor_datos.py'.
# 2. Tener instaladas las librerías necesarias.
#    Abre tu terminal y ejecuta:
#    pip install pandas plotly nbformat
#
# --------------------------------------------------------------------------

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio  # <--- IMPORTACIÓN AÑADIDA
import os

# --- CORRECCIÓN DE RENDERIZADO ---
# Se establece explícitamente el renderizador por defecto a 'browser'.
# Esto fuerza a Plotly a abrir el gráfico en una nueva pestaña del navegador
# y evita el error de 'nbformat' no encontrado.
pio.renderers.default = 'browser'

# --- CONFIGURACIÓN PRINCIPAL ---

# 1. Lista de criptomonedas que queremos comparar en el gráfico.
#    Deben coincidir con los nombres usados en el script de extracción.
ACTIVOS_A_COMPARAR = ['bitcoin', 'ethereum', 'solana', 'cardano']

# 2. Carpeta donde se encuentran los archivos CSV.
#    Debe ser la misma que la CARPETA_SALIDA_CSV del script anterior.
CARPETA_DATOS_CSV = 'grupo1/CRIPTOS_VARIOS/datos_criptomonedas_csv'

# 3. Moneda base para identificar la columna de precios.
MONEDA_COTIZACION = 'usd'


def cargar_y_normalizar_datos(lista_activos):
    """
    Carga los datos desde los archivos CSV, los normaliza para comparar
    rendimientos y los une en un solo DataFrame.

    La normalización consiste en convertir los precios a un rendimiento
    porcentual desde el primer día disponible en los datos.
    Fórmula: Rendimiento = ((Precio Actual / Precio Inicial) - 1) * 100

    Args:
        lista_activos (list): Una lista con los IDs de los activos a cargar.

    Returns:
        pandas.DataFrame: Un DataFrame con las fechas como índice y una
                          columna por cada activo con su rendimiento normalizado.
    """
    print("--- Cargando y Normalizando Datos ---")
    df_comparativo = pd.DataFrame()
    columna_precio = f'precio_{MONEDA_COTIZACION}'

    for activo_id in lista_activos:
        ruta_archivo = os.path.join(CARPETA_DATOS_CSV, f"{activo_id}_datos_historicos.csv")

        # Verificamos si el archivo CSV para el activo existe
        if not os.path.exists(ruta_archivo):
            print(f"ADVERTENCIA: No se encontró el archivo '{ruta_archivo}'. Se omitirá '{activo_id}'.")
            continue

        # Leemos el archivo CSV
        df_activo = pd.read_csv(ruta_archivo, index_col='fecha', parse_dates=True)

        # Normalización del precio
        precio_inicial = df_activo[columna_precio].iloc[0]
        rendimiento_normalizado = ((df_activo[columna_precio] / precio_inicial) - 1) * 100
        
        # Añadimos la serie de rendimiento al DataFrame comparativo
        df_comparativo[activo_id.capitalize()] = rendimiento_normalizado
        print(f"Datos de '{activo_id}' cargados y normalizados.")

    return df_comparativo


def generar_grafico_comparativo(df_datos):
    """
    Genera un gráfico de líneas interactivo usando Plotly a partir de
    un DataFrame de rendimientos normalizados.

    Args:
        df_datos (pandas.DataFrame): DataFrame con los datos a graficar.
    """
    print("\n--- Generando Gráfico Interactivo ---")
    fig = go.Figure()

    # Iteramos sobre cada columna (cada activo) del DataFrame
    for activo in df_datos.columns:
        fig.add_trace(go.Scatter(
            x=df_datos.index,
            y=df_datos[activo],
            mode='lines',
            name=activo  # El nombre que aparecerá en la leyenda
        ))

    # Personalizamos el diseño del gráfico
    fig.update_layout(
        title='Rendimiento Porcentual Comparativo de Criptomonedas',
        xaxis_title='Fecha',
        yaxis_title='Rendimiento Normalizado (%)',
        legend_title='Activos',
        template='plotly_dark',  # Un tema oscuro y moderno
        hovermode='x unified' # Mejora la experiencia al pasar el cursor
    )
    
    # Guardamos el gráfico en un archivo HTML interactivo
    nombre_archivo_html = 'grupo1/GRAFICOS_HTML/comparativa_rendimiento.html'
    fig.write_html(nombre_archivo_html)
    
    print(f"Gráfico guardado como '{nombre_archivo_html}'. Abriendo en el navegador...")
    
    # Mostramos el gráfico (se abrirá en una nueva pestaña del navegador)
    fig.show()


# --- Punto de Entrada del Script ---
if __name__ == "__main__":
    # 1. Cargar y procesar los datos
    datos_comparativos = cargar_y_normalizar_datos(ACTIVOS_A_COMPARAR)

    # 2. Generar el gráfico solo si se cargaron datos
    if not datos_comparativos.empty:
        generar_grafico_comparativo(datos_comparativos)
    else:
        print("\nNo se encontraron datos para graficar. Asegúrate de haber ejecutado primero el script de extracción.")
