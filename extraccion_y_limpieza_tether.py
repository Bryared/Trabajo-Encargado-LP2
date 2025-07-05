import subprocess
import sys
import json
import datetime
import os # Importar os para manejo de archivos

# --- Función para verificar e instalar dependencias ---
def instalar_paquete(nombre_paquete):
    try:
        __import__(nombre_paquete)
        print(f"'{nombre_paquete}' ya está instalado.")
    except ImportError:
        print(f"'{nombre_paquete}' no encontrado. Intentando instalar ahora...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", nombre_paquete])
            print(f"'{nombre_paquete}' instalado exitosamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar '{nombre_paquete}': {e}")
            print(f"Por favor, intenta ejecutar 'pip install {nombre_paquete}' manualmente en tu terminal.")
            sys.exit(1)

# --- Asegurarse de que pycoingecko esté instalado ---
instalar_paquete("pycoingecko")
from pycoingecko import CoinGeckoAPI

# --- Función de Extracción de Datos Históricos de Tether ---
def extraer_datos_historicos_tether(days_ago=365):
    cg = CoinGeckoAPI()
    coin_id = 'tether'
    vs_currency = 'usd'
    try:
        print(f"Obteniendo datos históricos de '{coin_id.capitalize()}' en '{vs_currency.upper()}' para los últimos {days_ago} días/periodo...")
        data = cg.get_coin_market_chart_by_id(coin_id, vs_currency, days=days_ago)
        if not data or 'prices' not in data:
            print(f"No se pudieron obtener datos históricos de precios para {coin_id}.")
            return None
        return data['prices']
    except Exception as e:
        print(f"Ocurrió un error durante la extracción de datos históricos: {e}")
        return None

# --- Función de Limpieza de Datos Históricos de Tether ---
def limpiar_datos_historicos_tether(raw_historical_data):
    """
    Limpieza y formatea los datos históricos brutos para análisis.
    Guarda el resultado en 'tether_cleaned_data.json'.
    """
    if not raw_historical_data:
        print("No hay datos históricos brutos para limpiar.")
        return None

    print("Iniciando la limpieza de datos históricos de Tether (USDT)...")
    cleaned_data_list = []
    for timestamp_ms, price in raw_historical_data:
        dt_object = datetime.datetime.fromtimestamp(timestamp_ms / 1000)
        cleaned_data_list.append({
            "fecha_utc": dt_object.strftime('%Y-%m-%d %H:%M:%S'),
            "precio_usd": price
        })

    with open('tether_cleaned_data.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_data_list, f, ensure_ascii=False, indent=4)
    print("Datos de Tether (USDT) limpiados y guardados en 'tether_cleaned_data.json'.")
    return cleaned_data_list

# --- Ejecución principal ---
if __name__ == "__main__":
    print("Iniciando el proceso de extracción y limpieza para generar 'tether_cleaned_data.json'...")
    raw_data = extraer_datos_historicos_tether(days_ago=365)
    if raw_data:
        limpiar_datos_historicos_tether(raw_data)
    else:
        print("No se pudieron generar los datos limpios porque la extracción falló.")
    print("Proceso de generación de datos limpios finalizado.")
