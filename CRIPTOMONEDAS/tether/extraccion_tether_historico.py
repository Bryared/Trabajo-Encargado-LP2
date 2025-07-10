import subprocess
import sys
import json
import datetime

# --- Función para verificar e instalar dependencias ---
def instalar_paquete(nombre_paquete):
    """
    Instala un paquete de Python si no está ya instalado.
    """
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

# --- Asegurarse de que pycoingecko esté instalado antes de intentar usarlo ---
instalar_paquete("pycoingecko")
from pycoingecko import CoinGeckoAPI

# --- Función principal de Extracción de Datos Históricos de Tether (USDT) ---
def extraer_datos_historicos_tether(days_ago=365):
    """
    Extrae datos históricos de Tether (USDT) en USD usando la API de CoinGecko.

    Args:
        days_ago (int): Número de días hacia atrás desde hoy para obtener los datos.

    Returns:
        list: Una lista de listas [timestamp_ms, price] o None si falla.
    """
    cg = CoinGeckoAPI()
    coin_id = 'tether'
    vs_currency = 'usd'
    try:
        print(f"Obteniendo datos históricos de '{coin_id.capitalize()}' en '{vs_currency.upper()}' para los últimos {days_ago} días/periodo...")
        data = cg.get_coin_market_chart_by_id(coin_id, vs_currency, days=days_ago)
        if not data or 'prices' not in data:
            print(f"No se pudieron obtener datos históricos de precios para {coin_id}.")
            return None
        return data['prices'] # Devuelve solo la lista de precios y timestamps
    except Exception as e:
        print(f"Ocurrió un error durante la extracción de datos históricos: {e}")
        return None

# --- Ejecución principal del script cuando se ejecuta directamente ---
if __name__ == "__main__":
    print("Iniciando el proceso de extracción de datos históricos de Tether (USDT)...")
    dias_a_obtener = 365 # Puedes cambiar esto para obtener más o menos días
    raw_data = extraer_datos_historicos_tether(days_ago=dias_a_obtener)
    if raw_data:
        print(f"Extracción de {len(raw_data)} puntos de datos completada.")
    print("Proceso de extracción de datos históricos de Tether (USDT) finalizado.")
