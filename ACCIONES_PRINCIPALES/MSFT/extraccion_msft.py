import requests
import json

# ========== EXTRACCIÓN DE DATOS PARA MICROSOFT ==========
API_KEY = "IHEB6GAC16MZIU36"
symbol = "MSFT"
url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&apikey={API_KEY}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    # Guardar archivo JSON directamente en carpeta MSFT
    with open("datos_crudos_MSFT.json", "w") as f:
        json.dump(data, f, indent=4)
    
    print("✅ Archivo 'datos_crudos_MSFT.json' guardado correctamente.")
else:
    print("❌ Error al obtener datos:", response.status_code)

