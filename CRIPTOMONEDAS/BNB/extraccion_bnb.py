# extraccion_bnb.py

import requests

ID_ACTIVO = "binancecoin"
API_URL = f"https://api.coingecko.com/api/v3/coins/{ID_ACTIVO}/market_chart"
PARAMS = {
    "vs_currency": "usd",
    "days": "30",
    "interval": "daily"
}

def extraer_datos():
    print("📡 Conectando a la API de CoinGecko...")
    response = requests.get(API_URL, params=PARAMS)
    
    if response.status_code != 200:
        print("❌ Error al acceder a la API:", response.status_code)
        print("Respuesta:", response.text)
        return None

    data = response.json()
    
    if "prices" not in data:
        print("❌ La respuesta no contiene datos de precios.")
        print("Respuesta:", data)
        return None

    return data["prices"]

if __name__ == "__main__":
    precios = extraer_datos()
    print(precios)
