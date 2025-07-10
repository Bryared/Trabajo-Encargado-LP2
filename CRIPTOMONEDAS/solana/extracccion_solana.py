import requests
import json
import os
import time

# --- 1. Identificar Endpoint y Parámetros ---
# El 'id' del activo en la API de CoinGecko.
ID_ACTIVO = "solana"
URL_ENDPOINT = f"https://api.coingecko.com/api/v3/coins/{ID_ACTIVO}/market_chart"
# Nombre del archivo para guardar los datos crudos.
NOMBRE_ARCHIVO_CRUDO = f"datos_crudos_{ID_ACTIVO}.json"

# Parámetros para la solicitud a la API.
# vs_currency: la moneda en la que queremos el precio (dólares estadounidenses).
# days: el número de días de datos históricos que queremos.
PARAMETROS = {
    'vs_currency': 'usd',
    'days': '365'
}

# Encabezado para simular una solicitud desde un navegador web.
# Esto ayuda a evitar bloqueos de la API o de firewalls (Causa común del error 10054).
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def extraer_datos_coingecko():
    """
    Se conecta a la API de CoinGecko, extrae los datos históricos de mercado
    para el activo especificado y los guarda en un archivo JSON crudo.
    """
    print(f"--- Iniciando Fase 1: Extracción de Datos para '{ID_ACTIVO}' ---")
    
    # --- 2. Realizar Solicitud ---
    try:
        print(f"Realizando solicitud a: {URL_ENDPOINT}")
        # Se añade el encabezado 'HEADERS' a la solicitud.
        # Se añade un 'timeout' para evitar que la solicitud se quede colgada indefinidamente.
        respuesta = requests.get(URL_ENDPOINT, params=PARAMETROS, headers=HEADERS, timeout=10)
        
        # Esta función lanzará un error si la solicitud no fue exitosa (ej. error 404 o 500).
        respuesta.raise_for_status()
        
    except requests.exceptions.RequestException as e:
        print(f"Error: No se pudo conectar a la API de CoinGecko. {e}")
        print("Esto puede deberse a un problema con tu conexión a internet, un firewall, o un problema temporal con la API.")
        return

    # --- 3. Procesar Respuesta ---
    # El código original tenía una verificación redundante. 
    # respuesta.raise_for_status() ya maneja los códigos de error, 
    # por lo que si el script llega aquí, el status_code es 2xx (exitoso).
    
    print(f"Respuesta recibida con éxito (Código de estado: {respuesta.status_code})")
    datos_json = respuesta.json()
    
    # b. Guardar JSON crudo
    try:
        # Usamos os.path.join para construir la ruta del archivo de forma segura.
        ruta_completa = os.path.join(os.path.dirname(__file__), NOMBRE_ARCHIVO_CRUDO)
        
        with open(ruta_completa, 'w', encoding='utf-8') as f:
            json.dump(datos_json, f, ensure_ascii=False, indent=4)
            
        print(f"Datos crudos guardados correctamente en: '{os.path.abspath(ruta_completa)}'")
        
    except IOError as e:
        print(f"Error al escribir en el archivo '{NOMBRE_ARCHIVO_CRUDO}': {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado al guardar el archivo: {e}")

# --- Punto de entrada del script ---
if __name__ == "__main__":
    extraer_datos_coingecko()
