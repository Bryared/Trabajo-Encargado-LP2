import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo con fechas y renombrar columna
df = pd.read_csv("datos_limpios_AAPL.csv", parse_dates=["Unnamed: 0"])
df.rename(columns={"Unnamed: 0": "Fecha"}, inplace=True)
df.set_index("Fecha", inplace=True)

# ----- Cálculo de métricas financieras -----

# Rendimiento mensual en porcentaje
df['rendimiento'] = df['adjusted_close'].pct_change() * 100

# Volatilidad móvil (desviación estándar de 3 meses)
df['volatilidad'] = df['rendimiento'].rolling(window=3).std()

# Filtrar solo meses con dividendos > 0
dividendos = df[df['dividend'] > 0]

# ----- GRÁFICO 1: Precio Ajustado -----
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['adjusted_close'], color='blue', marker='o', markersize=3, linewidth=1)
plt.title("Precio Ajustado de Apple (AAPL)")
plt.xlabel("Fecha")
plt.ylabel("Precio (USD)")
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("grafico_precio_AAPL.png")
plt.show()

# ----- GRÁFICO 2: Rendimiento Mensual -----
plt.figure(figsize=(10, 5))
plt.bar(df.index, df['rendimiento'], color='green', width=20)
plt.title("Rendimiento Mensual de AAPL (%)")
plt.xlabel("Fecha")
plt.ylabel("Rendimiento (%)")
plt.axhline(0, color='black', linewidth=1)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("grafico_rendimiento_AAPL.png")
plt.show()

# ----- ✅ GRÁFICO 3: Dividendos (CORREGIDO) -----
plt.figure(figsize=(10, 4))
plt.bar(dividendos.index, dividendos['dividend'], color='darkorchid', width=20)
plt.title("Dividendos Trimestrales de AAPL")
plt.xlabel("Fecha")
plt.ylabel("Dividendo por Acción (USD)")
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("grafico_dividendos_AAPL.png")
plt.show()
