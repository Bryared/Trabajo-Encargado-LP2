### 📈 Grupo 3: Acciones (AAPL, TSLA, NVDA)

* **Encargados**: Alexander, Marcelo, Victor Lopez.
* **Misión**: Analizar el sector tecnológico a través de tres de sus empresas más influyentes, obteniendo y limpiando sus datos bursátiles.
* **Flujo de Trabajo por Carpetas**:
    * **En `src/extraccion/`**: Construirán los scripts para conectarse a la API de acciones (yfinance, Alpha Vantage) y extraer los datos de Apple, Tesla y Nvidia.
    * **En `data/crudos/`**: Guardarán aquí las respuestas de la API en formato JSON.
    * **En `src/limpieza/`**: Se enfocarán en procesar los datos de las acciones, ajustando precios y estandarizando las fechas.
    * **En `data/limpios/`**: Producirán los CSV finales para cada acción, listos para el análisis comparativo.