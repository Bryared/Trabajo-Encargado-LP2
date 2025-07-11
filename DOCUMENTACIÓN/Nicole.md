# TESLA
# Extracción de Datos
Se realiza mediante una solicitud HTTP GET a la API de Financial Modeling Prep para obtener los precios históricos de las acciones de Tesla (TSLA).
```python
import requests
API_KEY = "TU_API_KEY"
symbol = "TSLA"

url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?serietype=line&timeseries=60&apikey={API_KEY}"

response = requests.get(url)
data = response.json()
```
✔️ Parámetros:

-symbol: símbolo de la acción (en este caso TSLA)

-timeseries: cantidad de datos históricos (últimos 60 registros)

-serietype=line: para recibir precios de cierre diarios/mensuales en serie lineal
# Limpieza y Preparación de Datos
Una vez obtenidos los datos, se convierten en un DataFrame de pandas y se preparan para su análisis.
```python
import pandas as pd
```
## Convertir a DataFrame
```python
df = pd.DataFrame(data["historical"])
```
## Convertir columna 'date' a tipo datetime
```python
df["date"] = pd.to_datetime(df["date"])
```
## Ordenar por fecha ascendente
```python
df = df.sort_values("date")
```
# Guardado del DataFrame
```python
Para tener un respaldo local, se guarda la serie de tiempo en un archivo CSV codificado en utf-8-sig (para compatibilidad con Excel).
df.to_csv("tesla_series_tiempo.csv", index=False, encoding="utf-8-sig")
print("📄 Archivo 'tesla_series_tiempo.csv' generado correctamente.")
```

Finalmente, presentamos toda la codificación:
```python
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

```
Apicaremos lo mismo en la siguiente extracción 
```python
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
```

Finalmente obtnemo graficas como : 

<img width="836" height="412" alt="image" src="https://github.com/user-attachments/assets/e8e32e03-27c3-4eed-8154-14705b0db704" />

<img width="826" height="412" alt="image" src="https://github.com/user-attachments/assets/85e8235e-ed47-4ba3-a7dd-66ae39c69918" />

