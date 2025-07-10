# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# PASO 0: IMPORTAR LAS HERRAMIENTAS NECESARIAS
# -----------------------------------------------------------------------------
# 'pandas' es una biblioteca fundamental para la manipulación y análisis de datos.
# La usaremos para crear y trabajar con nuestro "DataFrame", que es como una tabla de Excel.
import pandas as pd

# 'json' nos permite trabajar con archivos en formato JSON (JavaScript Object Notation),
# que es un formato muy común para intercambiar datos en la web.
import json

# 'os' (Operating System) nos da herramientas para interactuar con el sistema operativo,
# como por ejemplo, para manejar rutas de archivos y carpetas de una forma segura.
import os

# -----------------------------------------------------------------------------
# PASO 1: CONFIGURACIÓN DE RUTAS Y NOMBRES DE ARCHIVOS
# -----------------------------------------------------------------------------
# --- La solución al problema de la ruta ---
# La siguiente línea obtiene la ruta absoluta de la CARPETA donde se encuentra este script.
# __file__ es una variable especial que contiene la ruta del script actual.
# os.path.abspath() la convierte en una ruta completa (ej: C:\Users\...).
# os.path.dirname() extrae solo el directorio de esa ruta completa.
# De esta forma, no importa desde dónde ejecutes el script, siempre encontrará los archivos.
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))

# --- Definimos las variables para los nombres de nuestros archivos ---
ID_ACTIVO = "solana"

# Usamos os.path.join() para unir la ruta de nuestra carpeta con el nombre del archivo.
# Esto crea una ruta completa y correcta, evitando errores.
NOMBRE_ARCHIVO_CRUDO = os.path.join(DIRECTORIO_ACTUAL, f"datos_crudos_{ID_ACTIVO}.json")
NOMBRE_ARCHIVO_LIMPIO = os.path.join(DIRECTORIO_ACTUAL, f"datos_limpios_{ID_ACTIVO}.csv")

def limpiar_y_procesar_datos():
    """
    Esta función es el corazón del script. Se encarga de cargar los datos
    crudos desde el archivo JSON, los limpia, los transforma y finalmente
    guarda el resultado en un nuevo archivo CSV limpio.
    """
    print(f"\n--- Iniciando Fase 2: Limpieza y Procesamiento para '{ID_ACTIVO}' ---")

    # -------------------------------------------------------------------------
    # PASO 2: CARGAR LOS DATOS CRUDOS
    # -------------------------------------------------------------------------
    # Primero, validamos que el archivo JSON crudo realmente exista.
    # Si no existe, no podemos continuar.
    if not os.path.exists(NOMBRE_ARCHIVO_CRUDO):
        print(f"Error: El archivo '{os.path.basename(NOMBRE_ARCHIVO_CRUDO)}' no existe.")
        print("Por favor, ejecuta primero el script 'extraccion_solana.py'.")
        return # Detenemos la función si el archivo no se encuentra.
        
    # Usamos 'with open(...)', que es la forma segura de abrir archivos en Python.
    # Se asegura de que el archivo se cierre automáticamente, incluso si hay errores.
    # 'r' significa que lo abrimos en modo lectura (read).
    # 'encoding='utf-8'' es importante para manejar caracteres especiales.
    with open(NOMBRE_ARCHIVO_CRUDO, 'r', encoding='utf-8') as f:
        datos_crudos = json.load(f)
    
    # El archivo JSON de CoinGecko tiene una clave 'prices' que contiene la lista de precios.
    # Creamos un DataFrame de pandas a partir de esa lista.
    # Le decimos que la tabla tendrá dos columnas: 'timestamp' y 'price'.
    df = pd.DataFrame(datos_crudos['prices'], columns=['timestamp', 'price'])
    print("Datos cargados correctamente en un DataFrame.")

    # -------------------------------------------------------------------------
    # PASO 3: EXPLORAR Y ENTENDER LOS DATOS
    # -------------------------------------------------------------------------
    print("\nPrimeras 5 filas de los datos crudos:")
    print(df.head()) # .head() nos muestra una vista previa de las primeras filas.
    
    print("\nInformación general del DataFrame:")
    df.info() # .info() nos da un resumen técnico: tipos de datos, memoria, etc.

    # -------------------------------------------------------------------------
    # PASO 4: LIMPIEZA Y TRANSFORMACIÓN DE DATOS
    # -------------------------------------------------------------------------
    print("\nIniciando proceso de limpieza...")
    
    # a. Manejar valores nulos (vacíos)
    # Contamos cuántos valores nulos hay en total en el DataFrame.
    if df.isnull().sum().sum() > 0:
        print("Se encontraron valores nulos. Eliminando filas afectadas...")
        # .dropna() elimina las filas que contengan al menos un valor nulo.
        # 'inplace=True' modifica el DataFrame directamente sin necesidad de reasignarlo.
        df.dropna(inplace=True)
    else:
        print("No se encontraron valores nulos. ¡Excelente!")
        
    # b. Convertir la columna de tiempo a un formato legible
    # El 'timestamp' de la API viene en milisegundos. Lo convertimos a fecha y hora.
    # 'unit="ms"' le indica a pandas que el número representa milisegundos.
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    print("Columna 'timestamp' convertida a formato de fecha (datetime).")
    
    # c. Renombrar columnas para que sean más descriptivas
    df.rename(columns={
        'timestamp': 'Fecha',
        'price': 'Precio_USD'
    }, inplace=True)
    print("Columnas renombradas a 'Fecha' y 'Precio_USD'.")

    print("\nPrimeras 5 filas de los datos ya limpios y transformados:")
    print(df.head())

    # -------------------------------------------------------------------------
    # PASO 5: GUARDAR LOS DATOS LIMPIOS EN UN ARCHIVO CSV
    # -------------------------------------------------------------------------
    try:
        # .to_csv() exporta el DataFrame a un archivo CSV.
        # 'index=False' evita que pandas guarde el número de fila (índice) como una columna.
        df.to_csv(NOMBRE_ARCHIVO_LIMPIO, index=False, encoding='utf-8')
        # Usamos os.path.abspath() para mostrar la ruta completa donde se guardó el archivo.
        print(f"\n¡Éxito! Datos limpios guardados en: '{os.path.abspath(NOMBRE_ARCHIVO_LIMPIO)}'")
    except IOError as e:
        # Capturamos un posible error si no se puede escribir el archivo.
        print(f"Error al intentar guardar el archivo '{NOMBRE_ARCHIVO_LIMPIO}': {e}")

# -----------------------------------------------------------------------------
# PUNTO DE ENTRADA DEL SCRIPT
# -----------------------------------------------------------------------------
# Esta es una construcción estándar en Python.
# El código dentro de este 'if' solo se ejecutará cuando corras este archivo
# directamente (y no cuando lo importes desde otro script).
if __name__ == "__main__":
    limpiar_y_procesar_datos()