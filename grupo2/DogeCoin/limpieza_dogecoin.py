import pandas as pd
import json
import os

# --- Nombres de archivos ---
ID_ACTIVO = "dogecoin"
NOMBRE_ARCHIVO_CRUDO = f"datos_crudos_{ID_ACTIVO}.json"
NOMBRE_ARCHIVO_LIMPIO = f"datos_limpios_{ID_ACTIVO}.csv"

def limpiar_y_procesar_datos():
    """
    Carga los datos crudos desde el archivo JSON, los limpia, transforma
    y guarda el resultado en un archivo CSV limpio.
    """
    print(f"\n--- Iniciando Fase 2: Limpieza y Procesamiento para '{ID_ACTIVO}' ---")

    # --- 1. Cargar Datos ---
    # Validamos que el archivo crudo exista antes de continuar
    if not os.path.exists(NOMBRE_ARCHIVO_CRUDO):
        print(f"Error: El archivo '{NOMBRE_ARCHIVO_CRUDO}' no existe.")
        print("Por favor, ejecuta primero el script extraccion_'{ID_ACTIVO}'.py.")
        return
        
    with open(NOMBRE_ARCHIVO_CRUDO, 'r', encoding='utf-8') as f:
        datos_crudos = json.load(f)
    
    # Los datos de precios vienen en una lista llamada 'prices'
    # Creamos un DataFrame de pandas a partir de esta lista
    df = pd.DataFrame(datos_crudos['prices'], columns=['timestamp', 'price'])
    print("Datos cargados en un DataFrame de pandas.")

    # --- 2. Explorar DataFrame ---
    print("\nPrimeras 5 filas de los datos crudos:")
    print(df.head())
    print("\nInformación general del DataFrame:")
    df.info()

    # --- 3. Limpieza ---
    # a. Seleccionar columnas relevantes (hecho al crear el DataFrame)
    
    # b. Manejar nulos
    # Revisamos si hay valores nulos en nuestro DataFrame
    if df.isnull().sum().sum() > 0:
        print("\nSe encontraron valores nulos. Tratándolos...")
        # En este caso, la opción más simple es eliminar las filas con nulos
        df.dropna(inplace=True)
    else:
        print("\nNo se encontraron valores nulos.")
        
    # c. Convertir timestamps
    # El timestamp de CoinGecko viene en milisegundos. Lo convertimos a un formato de fecha legible.
    # 'unit="ms"' le indica a pandas cómo interpretar el número.
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    print("\nColumna 'timestamp' convertida a formato de fecha.")
    
    # d. Renombrar columnas a los nombres solicitados
    df.rename(columns={
        'timestamp': 'Fecha',
        'price': 'Precio_USD'
    }, inplace=True)
    print("Columnas renombradas a 'Fecha' y 'Precio_USD'.")

    print("\nPrimeras 5 filas de los datos limpios:")
    print(df.head())

    # --- 4. Guardar CSV limpio ---
    try:
        # 'index=False' evita que pandas guarde el índice del DataFrame en el CSV
        df.to_csv(NOMBRE_ARCHIVO_LIMPIO, index=False, encoding='utf-8')
        print(f"\nDatos limpios guardados correctamente en: '{os.path.abspath(NOMBRE_ARCHIVO_LIMPIO)}'")
    except IOError as e:
        print(f"Error al escribir en el archivo '{NOMBRE_ARCHIVO_LIMPIO}': {e}")

# --- Punto de entrada del script ---
if __name__ == "__main__":
    limpiar_y_procesar_datos()