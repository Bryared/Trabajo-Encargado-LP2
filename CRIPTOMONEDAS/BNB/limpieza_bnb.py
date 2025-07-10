# limpieza_bnb.py

import pandas as pd
from datetime import datetime

def limpiar_datos(precios_raw, archivo_csv="datos_limpios_binancecoin.csv"):
    print("🧹 Limpiando y estructurando datos...")
    datos = []
    for timestamp, precio in precios_raw:
        fecha = datetime.fromtimestamp(timestamp / 1000).date()
        if precio > 0:
            datos.append({
                "Fecha": fecha,
                "Precio_USD": round(precio, 2)
            })

    df = pd.DataFrame(datos)
    df.to_csv(archivo_csv, index=False)
    print(f"✅ Datos limpios guardados en: {archivo_csv}")
    return df
