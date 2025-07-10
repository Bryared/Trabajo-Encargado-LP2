# --------------------------------------------------------------------------
# SCRIPT 1: EXTRACTOR DE DATOS DE ACCIONES DESDE ALPHA VANTAGE
# --------------------------------------------------------------------------
#
# OBJETIVO:
# Este script se conecta a la API de Alpha Vantage para descargar el historial
# de precios mensuales ajustados de una lista de acciones y ETFs (como el S&P 500)
# y guarda los datos en archivos CSV individuales.
#
# PRERREQUISITOS:
# Antes de ejecutar, asegúrate de tener instaladas las librerías necesarias.
# Abre tu terminal o línea de comandos y ejecuta:
# pip install requests pandas
#
# --------------------------------------------------------------------------

import requests
import pandas as pd
import os
import time

# --- CONFIGURACIÓN PRINCIPAL ---

# 1. Tu clave de API de Alpha Vantage.
API_KEY = "IHEB6GAC16MZIU36"

# 2. Lista de símbolos (tickers) de acciones que queremos analizar.
#    Ejemplos: 'AAPL' (Apple), 'MSFT' (Microsoft), 'SPY' (ETF del S&P 500).
ACTIVOS_A_ANALIZAR = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'SPY', 'SILVER']

# 3. Nombre de la carpeta donde se guardarán los archivos CSV de acciones.
CARPETA_SALIDA_CSV = 'grupo1/ACTIVOS_GUIA/datos_acciones_csv'


def obtener_y_guardar_datos_historicos_acciones():
    """
    Función principal que recorre la lista de símbolos de acciones,
    obtiene los datos de Alpha Vantage y los guarda en archivos CSV.
    """
    print("--- Iniciando Proceso de Extracción de Datos de Acciones ---")

    # Crear la carpeta de salida si no existe
    if not os.path.exists(CARPETA_SALIDA_CSV):
        os.makedirs(CARPETA_SALIDA_CSV)
        print(f"Carpeta '{CARPETA_SALIDA_CSV}' creada con éxito.")

    for simbolo in ACTIVOS_A_ANALIZAR:
        print(f"\nProcesando: {simbolo}...")

        try:
            # --- Construcción del Endpoint y Petición a la API ---
            params = {
                "function": "TIME_SERIES_MONTHLY_ADJUSTED",
                "symbol": simbolo,
                "apikey": API_KEY
            }
            
            respuesta = requests.get("https://www.alphavantage.co/query", params=params)
            respuesta.raise_for_status()
            datos_json = respuesta.json()

            # Alpha Vantage puede devolver un mensaje de error o una nota sobre la frecuencia
            # de las llamadas en el JSON, incluso con una respuesta exitosa (código 200).
            if "Error Message" in datos_json:
                raise ValueError(f"Error de la API para {simbolo}: {datos_json['Error Message']}")
            if "Note" in datos_json:
                print(f"Nota de la API para {simbolo}: {datos_json['Note']}. Pausando para evitar límites.")
                time.sleep(60) # Pausa larga si se detecta una nota de límite
                continue # Saltar al siguiente activo

            # --- Procesamiento y Limpieza de Datos con Pandas ---
            
            # Los datos vienen bajo la clave 'Monthly Adjusted Time Series'
            datos_series_temporales = datos_json['Monthly Adjusted Time Series']
            
            # Convertimos el diccionario de datos en un DataFrame.
            # 'orient="index"' es clave porque las fechas son las llaves del diccionario.
            df = pd.DataFrame.from_dict(datos_series_temporales, orient='index')
            
            # Convertimos el índice (que son strings de fechas) a objetos datetime
            df.index = pd.to_datetime(df.index)
            
            # Alpha Vantage devuelve los datos del más reciente al más antiguo, los ordenamos.
            df.sort_index(inplace=True)
            
            # Seleccionamos solo la columna que nos interesa: el precio de cierre ajustado.
            # El '5. adjusted close' es el precio que tiene en cuenta dividendos y splits.
            df_final = df[['5. adjusted close']].copy()
            
            # Renombramos la columna para que sea más clara y la convertimos a tipo numérico.
            df_final.rename(columns={'5. adjusted close': 'precio_usd'}, inplace=True)
            df_final['precio_usd'] = pd.to_numeric(df_final['precio_usd'])

            # --- Guardado en Archivo CSV ---
            nombre_archivo = f"{CARPETA_SALIDA_CSV}/{simbolo}_datos_historicos.csv"
            df_final.to_csv(nombre_archivo)
            
            print(f"Datos guardados exitosamente en: '{nombre_archivo}'")

        except requests.exceptions.RequestException as e:
            print(f"ERROR de conexión para {simbolo}. Causa: {e}")
        except (KeyError, TypeError):
            print(f"ERROR: No se encontraron datos de series temporales para '{simbolo}'. "
                  "Verifica que el símbolo sea correcto o que no hayas excedido el límite de la API.")
        except ValueError as e:
            print(e)
            
        # PAUSA IMPORTANTE: La API gratuita de Alpha Vantage es muy estricta.
        # Permite ~5 llamadas por minuto. Hacemos una pausa de 15 segundos para estar seguros.
        print("Pausando por 15 segundos para respetar el límite de la API...")
        time.sleep(15)

    print("\n--- Proceso de Extracción de Acciones Finalizado ---")


if __name__ == "__main__":
    obtener_y_guardar_datos_historicos_acciones()
