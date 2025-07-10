import json
import os
import datetime # Needed to re-format dates if desired

def limpiar_datos_tether(input_file_path='tether_historical_data.json', output_file_path='tether_cleaned_data.json'):
    """
    Reads raw historical Tether (USDT) data from a JSON file,
    cleans and selects relevant information, and saves it to a new JSON file.

    Args:
        input_file_path (str): The path to the raw historical data JSON file.
        output_file_path (str): The path where the cleaned data will be saved.

    Returns:
        list: A list of dictionaries with the cleaned data, or None if an error occurs.
    """
    if not os.path.exists(input_file_path):
        print(f"Error: El archivo de entrada '{input_file_path}' no se encontró.")
        print("Asegúrate de haber ejecutado el script de extracción de Tether histórico primero.")
        return None

    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            raw_historical_data = json.load(f)

        if not raw_historical_data:
            print("El archivo de datos históricos brutos está vacío o corrupto.")
            return None

        cleaned_data = []
        for entry in raw_historical_data:
            fecha_utc = entry.get("fecha_utc")
            timestamp_ms = entry.get("timestamp_ms")
            precio_usd = entry.get("precio_usd")

            if fecha_utc and precio_usd is not None:
                cleaned_data.append({
                    "Fecha": fecha_utc,
                    "Precio_USD": precio_usd
                })

        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, ensure_ascii=False, indent=4)
        print(f"Datos de Tether (USDT) limpiados y guardados en '{output_file_path}'.")
        return cleaned_data

    except json.JSONDecodeError:
        print(f"Error: El archivo '{input_file_path}' no es un JSON válido o está corrupto.")
        return None
    except Exception as e:
        print(f"Ocurrió un error durante la limpieza de datos: {e}")
        return None

if __name__ == "__main__":
    print("Iniciando la limpieza de datos históricos de Tether (USDT)...")
    limpiar_datos_tether()
    print("Proceso de limpieza finalizado.")
