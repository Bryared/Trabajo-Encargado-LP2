import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

ID_ACTIVO = "bnb"
API_URL = f"https://api.coingecko.com/api/v3/coins/{ID_ACTIVO}/market_chart"
PARAMS = {
    "vs_currency": "usd",
    "days": "30",
    "interval": "daily"
}
CSV_LIMPIO = f"datos_limpios_{ID_ACTIVO}.csv"
GRAFICO_PATH = f"grafico_precio_{ID_ACTIVO}.png"

def extraer_datos():
    response = requests.get(API_URL, params=PARAMS)
    data = response.json()
    return data["prices"]

def limpiar_datos(precios_raw):
    datos = []
    for timestamp, precio in precios_raw:
        fecha = datetime.fromtimestamp(timestamp / 1000).date()
        if precio > 0:
            datos.append({"Fecha": fecha, "Precio_USD": round(precio, 2)})
    df = pd.DataFrame(datos)
    df.to_csv(CSV_LIMPIO, index=False)
    return df

def analizar_y_visualizar(df):
    print("\n📊 Estadísticas descriptivas de BNB:")
    print(df["Precio_USD"].describe())

    plt.figure(figsize=(12, 6))
    plt.plot(df["Fecha"], df["Precio_USD"], label="Precio BNB", color="#f3ba2f")
    plt.title("Evolución del Precio de BNB (últimos 30 días)")
    plt.xlabel("Fecha")
    plt.ylabel("Precio en USD")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(GRAFICO_PATH)
    plt.show()

    print(f"\n✅ CSV guardado como '{CSV_LIMPIO}'")
    print(f"✅ Gráfico guardado como '{GRAFICO_PATH}'")

if __name__ == "__main__":
    precios = extraer_datos()
    df_limpio = limpiar_datos(precios)
    analizar_y_visualizar(df_limpio)
