import pandas as pd
import matplotlib.pyplot as plt
import os

# hhh--- Nombre del archivo ---
ID_ACTIVO = "solana"
NOMBRE_ARCHIVO_LIMPIO = f"datos_limpios_{ID_ACTIVO}.csv"
NOMBRE_GRAFICO = f"grafico_precio_{ID_ACTIVO}.png"

def analizar_y_visualizar():
    """
    Carga los datos limpios, realiza un análisis descriptivo básico y
    genera una visualización del precio a lo largo del tiempo.
    """
    print(f"\n--- Iniciando Fase 3: Análisis y Visualización para '{ID_ACTIVO}' ---")

    # --- 1. Cargar CSV limpio ---
    if not os.path.exists(NOMBRE_ARCHIVO_LIMPIO):
        print(f"Error: El archivo '{NOMBRE_ARCHIVO_LIMPIO}' no existe.")
        print("Por favor, ejecuta primero el script 'limpieza_bitcoin.py'.")
        return
    
    # 'parse_dates' le dice a pandas que la columna 'Fecha' debe ser interpretada como una fecha
    df = pd.read_csv(NOMBRE_ARCHIVO_LIMPIO, parse_dates=['Fecha'])
    print("Datos limpios cargados.")

    # --- 2. Análisis Descriptivo ---
    print("\nAnálisis Descriptivo del Precio (USD):")
    # .describe() genera estadísticas fundamentales como media, desviación estándar, etc.
    print(df['Precio_USD'].describe())

    # --- 3. Visualización preliminar ---
    print("\nGenerando gráfico de línea del precio...")
    
    # Definimos el tamaño de la figura para que se vea bien
    plt.figure(figsize=(12, 6))
    
    # Graficamos la Fecha en el eje X y el Precio en el eje Y
    plt.plot(df['Fecha'], df['Precio_USD'], label=f'Precio de {ID_ACTIVO.capitalize()}', color='#f2a900')
    
    # Añadimos títulos y etiquetas para que el gráfico sea claro
    plt.title(f'Evolución del Precio de {ID_ACTIVO.capitalize()} (Últimos 365 días)', fontsize=16)
    plt.xlabel('Fecha', fontsize=12)
    plt.ylabel('Precio en USD', fontsize=12)
    plt.legend() # Muestra la etiqueta del 'plot'
    plt.grid(True) # Añade una cuadrícula para facilitar la lectura
    
    # Ajustamos el layout para evitar que los elementos se superpongan
    plt.tight_layout()

    # Guardamos el gráfico en un archivo
    plt.savefig(NOMBRE_GRAFICO)
    print(f"Gráfico guardado correctamente en: '{os.path.abspath(NOMBRE_GRAFICO)}'")
    
    # Mostramos el gráfico en una ventana
    plt.show()

    # --- 4. Validación interna ---
    print("\nRealizando validación interna de los datos...")
    if df['Precio_USD'].le(0).any():
        print("Alerta: Se han detectado precios menores o iguales a cero.")
    else:
        print("Validación correcta: Todos los precios son positivos.")

# --- Punto de entrada del script ---
if __name__ == "__main__":
    analizar_y_visualizar()