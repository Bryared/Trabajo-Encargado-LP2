import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd

# Leer el archivo CSV
ruta_csv = Path(__file__).parent / 'DogeCoin' / 'dogecoin_prices.csv'
df_precios = pd.read_csv(ruta_csv)

# Asegurarse de que la columna de fecha esté en formato datetime
df_precios['date'] = pd.to_datetime(df_precios['date'])  # Ajusta 'date' al nombre real de tu columna

# Crear el gráfico
plt.figure(figsize=(10,5))
plt.plot(df_precios['date'], df_precios['price_usd'], color='red')  # Ajusta 'price_usd' al nombre real de tu columna
plt.title('Precio histórico de Dogecoin')
plt.xlabel('Fecha')
plt.ylabel('Precio en USD')
plt.grid(True)
plt.tight_layout()
plt.show()

ruta_csv_bit = Path(__file__).parent / 'bitcoin' / 'bitcoin_prices.csv'
df_precios = pd.read_csv(ruta_csv_bit)


df_precios['date'] = pd.to_datetime(df_precios['date'])  # Ajusta 'date' al nombre real de tu columna

# Crear el gráfico
plt.figure(figsize=(10,5))
plt.plot(df_precios['date'], df_precios['price_usd'], color='red')  # Ajusta 'price_usd' al nombre real de tu columna
plt.title('Precio histórico de Bitcoin')
plt.xlabel('Fecha')
plt.ylabel('Precio en USD')
plt.grid(True)
plt.tight_layout()
plt.show()


ruta_csv_et = Path(__file__).parent / 'ethereum_COIN' / 'ethereum_prices.csv'
df_precios = pd.read_csv(ruta_csv_et)


df_precios['date'] = pd.to_datetime(df_precios['date'])  # Ajusta 'date' al nombre real de tu columna

# Crear el gráfico
plt.figure(figsize=(10,5))
plt.plot(df_precios['date'], df_precios['price_usd'], color='red')  # Ajusta 'price_usd' al nombre real de tu columna
plt.title('Precio histórico de ethereum')
plt.xlabel('Fecha')
plt.ylabel('Precio en USD')
plt.grid(True)
plt.tight_layout()
plt.show()

ruta_csv_so = Path(__file__).parent / 'solana' / 'datos_limpios_solana.csv'
df_precios = pd.read_csv(ruta_csv_so)

df_precios['date'] = pd.to_datetime(df_precios['date'])  # Ajusta 'date' al nombre real de tu columna

# Crear el gráfico
plt.figure(figsize=(10,5))
plt.plot(df_precios['date'], df_precios['price_usd'], color='red')  # Ajusta 'price_usd' al nombre real de tu columna
plt.title('Precio histórico de solana')
plt.xlabel('Fecha')
plt.ylabel('Precio en USD')
plt.grid(True)
plt.tight_layout()
plt.show()




