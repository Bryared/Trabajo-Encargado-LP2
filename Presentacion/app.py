import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go
from typing import List, Dict

# --- Configuración de la Página de Streamlit ---
st.set_page_config(
    page_title="Visualizador de Activos Financieros",
    layout="wide"
)

# --- Constantes ---
# Se construye una ruta absoluta a la carpeta de datos para evitar problemas.
try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FOLDER = os.path.join(SCRIPT_DIR, "datos_limpios")
except NameError:
    # Fallback por si __file__ no está definido (ej. en algunos notebooks)
    DATA_FOLDER = "datos_limpios"


# --- Funciones Principales ---

def obtener_activos_disponibles(base_folder_path: str) -> List[str]:
    """
    Escanea las subcarpetas 'acciones' y 'criptos' para encontrar archivos .csv
    y extrae los nombres de los activos.
    """
    activos = []
    subfolders = ["acciones", "criptos"]

    if not os.path.exists(base_folder_path):
        st.error(f"Error: La carpeta base '{base_folder_path}' no fue encontrada.")
        return activos

    for subfolder in subfolders:
        folder_path = os.path.join(base_folder_path, subfolder)
        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                if filename.endswith("_datos_historicos.csv"):
                    asset_name = filename.replace("_datos_historicos.csv", "")
                    activos.append(asset_name)
    
    if not activos:
        st.warning(f"No se encontraron archivos con el formato '*_datos_historicos.csv' en las subcarpetas 'acciones' o 'criptos' dentro de '{base_folder_path}'.")

    return sorted(activos)


def cargar_datos_activos(tickers_a_cargar: List[str], base_folder_path: str) -> Dict[str, pd.DataFrame]:
    """
    Carga los datos desde los archivos CSV para una lista de activos,
    buscando en las carpetas 'acciones' y 'criptos' y manejando sus formatos.
    """
    datos_cargados = {}
    for ticker in tickers_a_cargar:
        df = None
        path_accion = os.path.join(base_folder_path, "acciones", f"{ticker}_datos_historicos.csv")
        if os.path.exists(path_accion):
            try:
                df = pd.read_csv(path_accion, index_col=0, parse_dates=True)
            except Exception as e:
                st.error(f"Error al leer el archivo de acción {ticker}: {e}")
        else:
            path_cripto = os.path.join(base_folder_path, "criptos", f"{ticker}_datos_historicos.csv")
            if os.path.exists(path_cripto):
                try:
                    df = pd.read_csv(path_cripto, index_col='fecha', parse_dates=True)
                except Exception as e:
                    st.error(f"Error al leer el archivo de cripto {ticker}: {e}")
            else:
                st.warning(f"No se encontró el archivo para el activo: {ticker} ni en acciones ni en criptos.")
        
        if df is not None:
            if 'precio_usd' in df.columns:
                df = df.rename(columns={'precio_usd': 'close'})
                datos_cargados[ticker] = df
            else:
                st.warning(f"El archivo para {ticker} no contiene la columna 'precio_usd'.")

    return datos_cargados


def crear_grafico_precios(datos: Dict[str, pd.DataFrame]):
    """
    Crea un gráfico interactivo con Plotly con los activos seleccionados.
    """
    fig = go.Figure()

    for ticker, df in datos.items():
        if 'close' in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index, y=df['close'], mode='lines', name=ticker,
                hovertemplate=f'<b>{ticker}</b><br>Fecha: %{{x|%Y-%m-%d}}<br>Precio: %{{y:$,.2f}}<extra></extra>'
            ))

    fig.update_layout(
        title='Evolución de Precios de Cierre (Activos Seleccionados)',
        xaxis_title='Fecha', yaxis_title='Precio de Cierre (USD)',
        legend_title='Activos', template='plotly_white', height=600,
        xaxis=dict(
            rangeselector=dict(buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1a", step="year", stepmode="backward"),
                dict(step="all")
            ])),
            rangeslider=dict(visible=True), type="date"
        )
    )
    return fig


def mostrar_graficos_individuales(datos: Dict[str, pd.DataFrame]):
    """
    Muestra un gráfico individual para cada activo, organizados en dos columnas.
    """
    st.header("Gráficos Individuales de Todos los Activos")
    st.markdown("---")

    lista_activos = list(datos.items())
    
    for i in range(0, len(lista_activos), 2):
        col1, col2 = st.columns(2)

        # --- Gráfico en la Columna 1 ---
        ticker1, df1 = lista_activos[i]
        with col1:
            if 'close' in df1.columns:
                fig1 = go.Figure()
                fig1.add_trace(go.Scatter(
                    x=df1.index, y=df1['close'], mode='lines', name=ticker1,
                    hovertemplate=f'Precio: %{{y:$,.2f}}<extra></extra>', line=dict(width=2)
                ))
                fig1.update_layout(
                    title=f"Evolución de Precio para {ticker1}",
                    xaxis_title='Fecha', yaxis_title='Precio (USD)',
                    template='plotly_white', height=400, margin=dict(t=40, b=40)
                )
                st.plotly_chart(fig1, use_container_width=True)

        # --- Gráfico en la Columna 2 (si existe) ---
        if i + 1 < len(lista_activos):
            ticker2, df2 = lista_activos[i+1]
            with col2:
                if 'close' in df2.columns:
                    fig2 = go.Figure()
                    fig2.add_trace(go.Scatter(
                        x=df2.index, y=df2['close'], mode='lines', name=ticker2,
                        hovertemplate=f'Precio: %{{y:$,.2f}}<extra></extra>', line=dict(width=2)
                    ))
                    fig2.update_layout(
                        title=f"Evolución de Precio para {ticker2}",
                        xaxis_title='Fecha', yaxis_title='Precio (USD)',
                        template='plotly_white', height=400, margin=dict(t=40, b=40)
                    )
                    st.plotly_chart(fig2, use_container_width=True)


# --- Aplicación Streamlit ---

def main():
    """
    Función principal que ejecuta la aplicación Streamlit.
    """
    st.title("Visualizador de Activos Financieros")
    st.markdown("Esta aplicación te permite cargar y visualizar datos de **acciones** y **criptomonedas**.")

    activos_disponibles = obtener_activos_disponibles(DATA_FOLDER)
    
    if not activos_disponibles:
        st.warning("Aún no se encuentran activos. Revisa los mensajes de error si existen.")
        return

    # Carga los datos de TODOS los activos una sola vez
    todos_los_datos = cargar_datos_activos(activos_disponibles, DATA_FOLDER)

    st.sidebar.header("Configuración de Gráfico Consolidado")
    activos_seleccionados = st.sidebar.multiselect(
        label="Selecciona los activos a comparar:",
        options=activos_disponibles,
        default=activos_disponibles[:2] if len(activos_disponibles) > 1 else activos_disponibles
    )

    # Filtra los datos para el gráfico consolidado según la selección
    datos_filtrados = {ticker: df for ticker, df in todos_los_datos.items() if ticker in activos_seleccionados}

    if not datos_filtrados:
        st.info("Por favor, selecciona al menos un activo en la barra lateral para ver el gráfico consolidado.")
    else:
        st.header("Gráfico Consolidado")
        figura_precios = crear_grafico_precios(datos_filtrados)
        st.plotly_chart(figura_precios, use_container_width=True)

    # Muestra los gráficos individuales de TODOS los activos, independientemente de la selección
    if todos_los_datos:
        mostrar_graficos_individuales(todos_los_datos)

        st.header("Datos en Bruto (Activos Seleccionados)")
        for ticker, df in datos_filtrados.items():
            with st.expander(f"Mostrar datos de {ticker}"):
                st.dataframe(df)

if __name__ == "__main__":
    main()
