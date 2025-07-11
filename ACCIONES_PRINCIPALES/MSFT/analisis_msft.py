import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV con fechas y convertir la columna de fechas al formato datetime
df = pd.read_csv("datos_limpios_MSFT.csv", parse_dates=["Unnamed: 0"])

# Renombrar la columna de fecha
df.rename(columns={"Unnamed: 0": "Fecha"}, inplace=True)

# Usar la columna 'Fecha' como índice del DataFrame
df.set_index("Fecha", inplace=True)

# ----- Cálculo de métricas financieras -----

# Calcular el rendimiento mensual (variación porcentual del precio ajustado)
df['rendimiento'] = df['adjusted_close'].pct_change() * 100

# Calcular la volatilidad como la desviación estándar móvil de 3 meses del rendimiento
df['volatilidad'] = df['rendimiento'].rolling(window=3).std()

# Filtrar solo los meses en los que se pagaron dividendos (mayores a 0)
dividendos = df[df['dividend'] > 0]

# ----- GRÁFICO 1: Precio Ajustado -----
plt.figure(figsize=(10, 5))  # Crear una figura de 10x5 pulgadas
plt.plot(df.index, df['adjusted_close'], color='blue', marker='o', markersize=3, linewidth=1)  # Línea del precio ajustado
plt.title("Precio Ajustado de Apple (AAPL)")  # Título del gráfico
plt.xlabel("Fecha")  # Etiqueta del eje X
plt.ylabel("Precio (USD)")  # Etiqueta del eje Y
plt.grid(True, linestyle='--', alpha=0.5)  # Agregar cuadrícula suave
plt.tight_layout()  # Ajustar márgenes del gráfico
plt.savefig("grafico_precio_AAPL.png")  # Guardar el gráfico como imagen
plt.show()  # Mostrar el gráfico

# ----- GRÁFICO 2: Rendimiento Mensual -----
plt.figure(figsize=(10, 5))  # Crear figura
plt.bar(df.index, df['rendimiento'], color='green', width=20)  # Gráfico de barras del rendimiento mensual
plt.title("Rendimiento Mensual de AAPL (%)")  # Título del gráfico
plt.xlabel("Fecha")  # Etiqueta del eje X
plt.ylabel("Rendimiento (%)")  # Etiqueta del eje Y
plt.axhline(0, color='black', linewidth=1)  # Línea horizontal en 0
plt.grid(True, linestyle='--', alpha=0.5)  # Cuadrícula
plt.tight_layout()  # Ajuste de márgenes
plt.savefig("grafico_rendimiento_AAPL.png")  # Guardar gráfico
plt.show()  # Mostrar gráfico

# ----- ✅ GRÁFICO 3: Dividendos (CORREGIDO) -----
plt.figure(figsize=(10, 4))  # Crear figura
plt.bar(dividendos.index, dividendos['dividend'], color='darkorchid', width=20)  # Barras de dividendos
plt.title("Dividendos Trimestrales de AAPL")  # Título
plt.xlabel("Fecha")  # Etiqueta eje X
plt.ylabel("Dividendo por Acción (USD)")  # Etiqueta eje Y
plt.grid(axis='y', linestyle='--', alpha=0.5)  # Cuadrícula solo en eje Y
plt.tight_layout()  # Ajustar márgenes
plt.savefig("grafico_dividendos_AAPL.png")  # Guardar gráfico
plt.show()  # Mostrar gráfico
