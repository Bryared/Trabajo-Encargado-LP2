### 🥇 Grupo 1: Activos Guía (BTC y SP500)

* **Encargados**: Ale, Nicole, Andrew, Bryan.
* **Misión**: Encargarse de los activos más representativos del mercado cripto y tradicional para establecer una base de comparación.
* **Flujo de Trabajo por Carpetas**:
    * **En `src/extraccion/`**: Desarrollarán los scripts para conectarse a las APIs (CoinGecko, yfinance) y descargar la información histórica de BTC y SP500.
    * **En `data/crudos/`**: Sus scripts de extracción guardarán aquí los datos originales (JSON) sin procesar.
    * **En `src/limpieza/`**: Crearán los scripts que toman esos datos crudos, seleccionan las columnas importantes, manejan valores nulos y estandarizan los formatos.
    * **En `data/limpios/`**: Aquí guardarán los datos ya procesados en formato CSV, listos para que el equipo de liderazgo los use en el análisis final.