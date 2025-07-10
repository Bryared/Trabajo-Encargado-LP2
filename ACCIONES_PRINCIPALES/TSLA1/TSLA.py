´´´python
import requests
import pandas as pd

# API Key
API_KEY = "DTDu0SOfs4dX4sJgaRSc4FAx7KPzHYBt"
symbol = "TSLA"

# Endpoint de histórico de precios mensual
url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?serietype=line&timeseries=60&apikey={API_KEY}"

# Consultar datos
response = requests.get(url)
data = response.json()

# Convertir a DataFrame
df = pd.DataFrame(data["historical"])

# Convertir columna date a datetime
df["date"] = pd.to_datetime(df["date"])

# Ordenar por fecha
df = df.sort_values("date")

# Mostrar
print(df)

# Guardar CSV
df.to_csv("tesla_series_tiempo.csv", index=False, encoding="utf-8-sig")
print("📄 Archivo 'tesla_series_tiempo.csv' generado correctamente.")
´´´ 
