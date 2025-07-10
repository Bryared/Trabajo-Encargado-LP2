import subprocess
import sys
import json
import os
import datetime # Used for date formatting if needed, though pandas handles most of it

# --- Función para verificar e instalar dependencias ---
def instalar_paquete(nombre_paquete):
    """
    Installs a Python package if it's not already installed.
    """
    try:
        __import__(nombre_paquete)
        print(f"'{nombre_paquete}' ya está instalado.")
    except ImportError:
        print(f"'{nombre_paquete}' no encontrado. Intentando instalar ahora...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", nombre_paquete])
            print(f"'{nombre_paquete}' instalado exitosamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar '{nombre_paquete}': {e}")
            print(f"Por favor, intenta ejecutar 'pip install {nombre_paquete}' manualmente en tu terminal.")
            sys.exit(1) # Exit the script if installation fails

# --- Ensure necessary libraries are installed ---
# These are essential for data manipulation (pandas) and plotting (matplotlib)
instalar_paquete("pandas")
instalar_paquete("matplotlib")

# Now that we know the libraries are installed, we can import them
import pandas as pd
import matplotlib.pyplot as plt

# --- Function for Historical Tether Data Analysis ---
def analizar_datos_historicos_tether(file_path='tether_cleaned_data.json'):
    """
    Reads the cleaned historical Tether data, performs basic analysis,
    and displays key statistics and a plot.

    Args:
        file_path (str): Path to the JSON file with the cleaned historical data.
    """
    # Check if the cleaned data file exists
    if not os.path.exists(file_path):
        print(f"Error: El archivo '{file_path}' no se encontró.")
        print("Asegúrate de haber ejecutado el script de extracción y limpieza (como 'generar_datos_limpios_tether.py') previamente para crear este archivo.")
        return

    try:
        # Load the cleaned data from the JSON file
        with open(file_path, 'r', encoding='utf-8') as f:
            datos_limpios = json.load(f)

        if not datos_limpios:
            print("El archivo de datos limpios está vacío o corrupto.")
            return

        # Convert the list of dictionaries into a Pandas DataFrame
        df = pd.DataFrame(datos_limpios)

        # Convert the 'fecha_utc' column to datetime objects and set it as the DataFrame index
        # This is crucial for time-series analysis and plotting
        df['fecha_utc'] = pd.to_datetime(df['fecha_utc'])
        df = df.set_index('fecha_utc')

        # Ensure the 'precio_usd' column is numeric
        df['precio_usd'] = pd.to_numeric(df['precio_usd'])

        print(f"\n--- Análisis de Datos Históricos de Tether (USDT) ---")
        print(f"Período de datos: Desde {df.index.min().strftime('%Y-%m-%d %H:%M')} hasta {df.index.max().strftime('%Y-%m-%d %H:%M')}")
        print(f"Número total de puntos de datos: {len(df)}")

        print("\n### Estadísticas Descriptivas del Precio (USD):")
        # Use .describe() for quick statistics and format to 4 decimal places for currency
        print(df['precio_usd'].describe().apply(lambda x: f"${x:,.4f}"))

        # Calculate specific key metrics
        min_price = df['precio_usd'].min()
        max_price = df['precio_usd'].max()
        avg_price = df['precio_usd'].mean()
        std_dev_price = df['precio_usd'].std() # Standard deviation to see volatility

        print(f"\n--- Resumen Clave del Precio de USDT (USD) ---")
        print(f"Precio Mínimo Observado (en el período): **${min_price:,.4f}**")
        print(f"Precio Máximo Observado (en el período): **${max_price:,.4f}**")
        print(f"Precio Promedio (Media) en el período: **${avg_price:,.4f}**")
        print(f"Desviación Estándar del Precio: **${std_dev_price:,.4f}** (Indica la volatilidad)")

        # Analyze stability given it's a stablecoin
        rango_precio = max_price - min_price
        print(f"Rango de Fluctuación (Máximo - Mínimo): **${rango_precio:,.4f}**")
        print(f"\n**Observación Importante sobre USDT:**")
        print(f"Dada su naturaleza de stablecoin, el precio de USDT debería idealmente mantenerse muy cercano a $1.00 USD.")
        if rango_precio > 0.005 or std_dev_price > 0.001: # Example thresholds for noticing significant deviation
            print(f"**¡Alerta!** El rango de fluctuación (${rango_precio:,.4f}) o la desviación estándar (${std_dev_price:,.4f}) son mayores de lo esperado para una stablecoin perfectamente anclada.")
            print(f"Esto podría indicar momentos de leve desvinculación ('depeg') del USD en el período analizado. Investiga las causas si estos valores son significativos.")
        else:
            print("El precio de USDT ha mostrado una excelente estabilidad, manteniéndose muy cerca de $1.00 USD en el período.")

        # --- Plotting the Historical Price ---
        plt.figure(figsize=(14, 7)) # Adjust figure size for better readability
        plt.plot(df.index, df['precio_usd'], label='Precio de USDT (USD)', color='skyblue', linewidth=1.5)
        plt.axhline(y=1.00, color='red', linestyle='--', label='Valor Objetivo ($1.00)', alpha=0.7) # Reference line at $1.00
        plt.title('Precio Histórico de Tether (USDT) vs. USD (Último Año)', fontsize=16)
        plt.xlabel('Fecha', fontsize=12)
        plt.ylabel('Precio (USD)', fontsize=12)
        plt.grid(True, linestyle=':', alpha=0.7) # Add a subtle grid
        plt.legend(fontsize=10)
        plt.xticks(rotation=45) # Rotate date labels for better readability
        plt.tight_layout() # Adjust layout to prevent labels from overlapping
        plt.show() # Display the plot

    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no se encontró. Asegúrate de que el archivo 'tether_cleaned_data.json' existe en la misma carpeta que este script.")
    except json.JSONDecodeError:
        print(f"Error: El archivo '{file_path}' no es un JSON válido o está corrupto. Verifica su contenido.")
    except KeyError as e:
        print(f"Error en la estructura de los datos: Falta la columna esperada '{e}'.")
        print(f"Asegúrate de que 'tether_cleaned_data.json' contiene las claves 'fecha_utc' y 'precio_usd'.")
    except Exception as e:
        print(f"Ocurrió un error inesperado durante el análisis: {e}")

# --- Main script execution ---
if __name__ == "__main__":
    print("Iniciando el análisis de datos históricos de Tether (USDT)...")
    analizar_datos_historicos_tether(file_path='tether_cleaned_data.json')
    print("Análisis de datos históricos de Tether (USDT) finalizado.")
