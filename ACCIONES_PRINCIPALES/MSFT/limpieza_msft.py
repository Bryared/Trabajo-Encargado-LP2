import pandas as pd
import json

# ========== CARGAR DATOS CRUDOS ==========
with open("datos_crudos_MSFT.json", "r") as f:
    data = json.load(f)

# Verifica que exista la clave esperada
if "Monthly Adjusted Time Series" not in data:
    print("❌ Estructura del JSON inválida o API sin datos.")
    exit()

# ========== LIMPIEZA Y TRANSFORMACIÓN ==========
raw_data = data['Monthly Adjusted Time Series']

# Convertir a DataFrame
df = pd.DataFrame.from_dict(raw_data, orient='index')

# Renombrar columnas
df.columns = ['open', 'high', 'low', 'close', 'adjusted_close', 'volume', 'dividend']

# Convertir tipos de datos a float
df = df.astype(float)

# Convertir índice a fechas y ordenar
df.index = pd.to_datetime(df.index)
df = df.sort_index()

# Guardar CSV limpio en la misma carpeta
df.to_csv("datos_limpios_MSFT.csv")

print("✅ Archivo 'datos_limpios_MSFT.csv' guardado correctamente.")
