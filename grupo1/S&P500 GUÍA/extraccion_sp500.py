import requests
import json
import os

# --- 1. Identificar Endpoint y Parámetros ---
# El 'id' para Bitcoin en la API de CoinGecko es "bitcoin"
ID_ACTIVO = "bitcoin"
URL_ENDPOINT = f"https://api.coingecko.com/api/v3/coins/{ID_ACTIVO}/market_chart"
# Nombre del archivo para guardar los datos crudos
NOMBRE_ARCHIVO_CRUDO = f"datos_crudos_{ID_ACTIVO}.json"

# Parámetros para la solicitud a la API
# vs_currency: la moneda en la que queremos el precio (dólares estadounidenses)
# days: el número de días de datos históricos que queremos
PARAMETROS = {
    'vs_currency': 'usd',
    'days': '365'
}

def extraer_datos_coingecko():
    """
    Se conecta a la API de CoinGecko, extrae los datos históricos de mercado
    para Bitcoin y los guarda en un archivo JSON crudo.
    """
    print(f"--- Iniciando Fase 1: Extracción de Datos para '{ID_ACTIVO}' ---")
    
    # --- 2. Realizar Solicitud ---
    try:
        print(f"Realizando solicitud a: {URL_ENDPOINT}")
        respuesta = requests.get(URL_ENDPOINT, params=PARAMETROS)
        # Esta función lanzará un error si la solicitud no fue exitosa (ej. error 404 o 500)
        respuesta.raise_for_status()
        
    except requests.exceptions.RequestException as e:
        print(f"Error: No se pudo conectar a la API de CoinGecko. {e}")
        return

    # --- 3. Procesar Respuesta ---
    # a. Verificar status_code
    if respuesta.status_code == 200:
        print("Respuesta recibida con éxito (Código de estado: 200)")
        datos_json = respuesta.json()
        
        # b. Guardar JSON crudo
        try:
            with open(NOMBRE_ARCHIVO_CRUDO, 'w', encoding='utf-8') as f:
                json.dump(datos_json, f, ensure_ascii=False, indent=4)
            print(f"Datos crudos guardados correctamente en: '{os.path.abspath(NOMBRE_ARCHIVO_CRUDO)}'")
        except IOError as e:
            print(f"Error al escribir en el archivo '{NOMBRE_ARCHIVO_CRUDO}': {e}")
            
    else:
        print(f"Error: La API devolvió un código de estado inesperado: {respuesta.status_code}")
        print(f"Respuesta: {respuesta.text}")

# --- Punto de entrada del script ---
if __name__ == "__main__":
    extraer_datos_coingecko()