# --------------------------------------------------------------------------
# FASE 1 y 2: EXTRACTOR DE DATOS DE CRIPTOMONEDAS DESDE COINGECKO
# --------------------------------------------------------------------------
#
# OBJETIVO:
# Este script se conecta a la API de CoinGecko para descargar el historial de
# precios de una lista de criptomonedas y guarda los datos en archivos CSV
# individuales para su posterior análisis y visualización.
#
# PRERREQUISITOS:
# Antes de ejecutar, asegúrate de tener instaladas las librerías necesarias.
# Abre tu terminal o línea de comandos y ejecuta:
# pip install requests pandas
#
# --------------------------------------------------------------------------

import requests  # Para realizar las peticiones HTTP a la API.
import pandas as pd  # Para manipular los datos y guardarlos en CSV.
import os  # Para interactuar con el sistema de archivos (crear carpetas).
import time  # Para añadir pausas y no sobrecargar la API.

# --- CONFIGURACIÓN PRINCIPAL ---

# 1. URL base de la API de CoinGecko. Todas las peticiones parten de aquí.
URL_BASE_API = "https://api.coingecko.com/api/v3"

# 2. Lista de criptomonedas que queremos analizar.
#    IMPORTANTE: Debemos usar el 'id' que CoinGecko asigna a cada activo,
#    no su ticker. Ej: 'bitcoin', no 'BTC'.
ACTIVOS_A_ANALIZAR = ['bitcoin', 'ethereum', 'solana', 'cardano', 'dogecoin']

# 3. Moneda en la que queremos los datos (dólares, euros, etc.).
MONEDA_COTIZACION = 'usd'

# 4. Período de datos históricos. 'max' para obtener todos los datos disponibles.
#    También puedes usar un número de días, como '365' para el último año.
DIAS_HISTORIAL = '365'

# 5. Nombre de la carpeta donde se guardarán los archivos CSV.
CARPETA_SALIDA_CSV = 'grupo1/CRIPTOS_VARIOS/datos_criptomonedas_csv'


def obtener_y_guardar_datos_historicos():
    # Función principal que recorre la lista de activos, obtiene los datos de CoinGecko y los guarda en archivos CSV.

    print("--- Iniciando el Proceso de Extracción de Datos ---")

    # Crear la carpeta de salida si no existe
    if not os.path.exists(CARPETA_SALIDA_CSV):
        os.makedirs(CARPETA_SALIDA_CSV)
        print(f"Carpeta '{CARPETA_SALIDA_CSV}' creada con éxito.")

    # Iteramos sobre cada activo de nuestra lista de configuración
    for activo_id in ACTIVOS_A_ANALIZAR:
        print(f"\nProcesando: {activo_id.capitalize()}...")

        try:
            # --- Construcción del Endpoint y Petición a la API ---

            # Este es el endpoint específico para obtener datos históricos del mercado.
            # Se construye dinámicamente para cada activo.
            url_endpoint = f"{URL_BASE_API}/coins/{activo_id}/market_chart"

            # Parámetros que enviaremos en la petición GET.
            # La API de CoinGecko los usa para filtrar la respuesta.
            params = {
                'vs_currency': MONEDA_COTIZACION,
                'days': DIAS_HISTORIAL,
                'interval': 'daily' # Datos diarios para no sobrecargar
            }

            # Realizamos la petición GET a la API.
            respuesta = requests.get(url_endpoint, params=params)
            
            # Verificamos si la petición fue exitosa (código de estado 200).
            # Si no, lanzamos un error para pasar al siguiente activo.
            respuesta.raise_for_status()
            
            datos_json = respuesta.json()
            print(f"Datos de {activo_id.capitalize()} obtenidos correctamente.")

            # --- Procesamiento y Limpieza de Datos con Pandas ---

            # La API devuelve los precios, capitalizaciones y volúmenes en listas separadas.
            # Extraemos la lista de precios. Cada elemento es [timestamp, precio].
            precios = datos_json['prices']

            # Creamos un DataFrame de Pandas a partir de la lista de precios.
            df = pd.DataFrame(precios, columns=['timestamp', 'precio'])

            # Convertimos la columna 'timestamp' (en milisegundos) a un formato
            # de fecha legible (Año-Mes-Día).
            df['fecha'] = pd.to_datetime(df['timestamp'], unit='ms').dt.date

            # Seleccionamos y reordenamos las columnas que nos interesan.
            df_final = df[['fecha', 'precio']]
            
            # Establecemos la columna 'fecha' como el índice del DataFrame.
            df_final.set_index('fecha', inplace=True)
            
            # Renombramos la columna 'precio' para que sea más descriptiva.
            df_final.rename(columns={'precio': f'precio_{MONEDA_COTIZACION}'}, inplace=True)

            # --- Guardado en Archivo CSV ---

            # Creamos un nombre de archivo dinámico para cada activo.
            nombre_archivo = f"{CARPETA_SALIDA_CSV}/{activo_id}_datos_historicos.csv"
            
            # Guardamos el DataFrame en un archivo CSV.
            df_final.to_csv(nombre_archivo)
            
            print(f"Datos guardados exitosamente en: '{nombre_archivo}'")

        except requests.exceptions.RequestException as e:
            # Capturamos posibles errores de conexión o de la API (ej: activo no encontrado).
            print(f"ERROR: No se pudieron obtener los datos para {activo_id}. Causa: {e}")
        
        except KeyError:
            # Capturamos un error común si la API no devuelve la llave 'prices'.
            print(f"ERROR: La respuesta de la API para {activo_id} no contiene datos de precios.")

        # Añadimos una pequeña pausa entre peticiones para ser respetuosos con la API
        # y evitar bloqueos por exceso de solicitudes.
        time.sleep(5)

    print("\n--- Proceso de Extracción Finalizado ---")


# --- Punto de Entrada del Script ---
# El código dentro de este 'if' solo se ejecutará cuando corras este archivo
# directamente desde la terminal.
if __name__ == "__main__":
    obtener_y_guardar_datos_historicos()
