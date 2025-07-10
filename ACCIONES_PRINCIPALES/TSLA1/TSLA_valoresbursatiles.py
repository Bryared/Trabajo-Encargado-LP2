import requests
import pandas as pd
import time

# Tu API Key
API_KEY = "DTDu0SOfs4dX4sJgaRSc4FAx7KPzHYBt"
symbol = "TSLA"

# Endpoints
profile_url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={API_KEY}"
balance_url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{symbol}?limit=1&apikey={API_KEY}"
income_url = f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}?limit=1&apikey={API_KEY}"
cashflow_url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{symbol}?limit=1&apikey={API_KEY}"

# Consultas a la API
profile_data = requests.get(profile_url).json()[0]
balance_data = requests.get(balance_url).json()[0]
income_data = requests.get(income_url).json()[0]
cashflow_data = requests.get(cashflow_url).json()[0]

# Combinar todos los datos en un solo diccionario
data = {**profile_data, **balance_data, **income_data, **cashflow_data}

# Crear un DataFrame
df = pd.DataFrame([data])

# Guardar como CSV
df.to_csv("TSLA_full_data.csv", index=False, encoding="utf-8-sig")

# Confirmar
print("📄 Archivo 'TSLA_full_data.csv' generado correctamente.")
