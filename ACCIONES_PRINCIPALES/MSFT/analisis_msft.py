import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo limpio
df = pd.read_csv("datos_limpios_MSFT.csv", parse_dates=["Unnamed: 0"])
df.rename(columns={"Unnamed: 0": "Fecha"}, inplace=True)
df.set_index("Fecha", inplace=True)

# Calcular rendimiento mensual (%)
df['rendimiento'] = df['adjusted_close'].pct_change() * 100

# Calcular volatilidad móvil (desviación estándar de 3 meses)
df['volatilidad'] = df['rendimiento'].rolling(window=3).std()

# Filtrar meses con dividendos
dividendos = df[df['dividend'] > 0]

# --------- GRÁFICO 1: Precio Ajustado ----------
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['adjusted_close'], color='blue', marker='o')
plt.title("Precio Ajustado de Microsoft (MSFT)")
plt.xlabel("Fecha")
plt.ylabel("Precio USD")
plt.grid(True)
plt.tight_layout()
plt.savefig("grafico_precio_msft.png")
plt.show()

# --------- GRÁFICO 2: Rendimiento Mensual ----------
plt.figure(figsize=(10, 5))
plt.bar(df.index, df['rendimiento'], color='green')
plt.title("Rendimiento Mensual de MSFT (%)")
plt.xlabel("Fecha")
plt.ylabel("Rendimiento (%)")
plt.axhline(0, color='black', linewidth=1)
plt.grid(True)
plt.tight_layout()
plt.savefig("grafico_rendimiento_msft.png")
plt.show()

# --------- GRÁFICO 3: Dividendos ----------
plt.figure(figsize=(10, 4))
plt.bar(dividendos.index, dividendos['dividend'], color='purple')
plt.title("Dividendos de MSFT")
plt.xlabel("Fecha")
plt.ylabel("Dividendo (USD)")
plt.tight_layout()
plt.savefig("grafico_dividendos_msft.png")
plt.show()
