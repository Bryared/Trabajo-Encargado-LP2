import requests
import pandas as pd
import time

API_KEY = "DTDu0SOfs4dX4sJgaRSc4FAx7KPzHYBt"
SYMBOLS = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]

balance_url = "https://financialmodelingprep.com/api/v3/balance-sheet-statement/{symbol}?limit=1&apikey=" + API_KEY
profile_url = "https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey=" + API_KEY

datos = []

for symbol in SYMBOLS:
    print(f"Procesando {symbol}")

    # Balance Sheet
    balance_response = requests.get(balance_url.format(symbol=symbol))
    balance_data = balance_response.json()
    total_assets = balance_data[0].get("totalAssets") if balance_data else None

    # Company Profile
    profile_response = requests.get(profile_url.format(symbol=symbol))
    profile_data = profile_response.json()
    market_cap = profile_data[0].get("mktCap") if profile_data else None
    name = profile_data[0].get("companyName") if profile_data else None

    datos.append({
        "symbol": symbol,
        "name": name,
        "totalAssets": total_assets,
        "marketCap": market_cap
    })

    time.sleep(1)  # para evitar sobrecargar la API

# Crear DataFrame
df = pd.DataFrame(datos)
print(df)

# Guardar CSV
df.to_csv("empresas_activos_marketcap.csv", index=False, encoding="utf-8-sig")
print("📄 Archivo 'empresas_activos_marketcap.csv' generado.")
