## 📊 Plan de Proyecto Detallado

### 🎯 Título del Proyecto

**"Análisis Cuantitativo de Riesgo y Rendimiento en Mercados Modernos"**

### 🔍 Activos a Analizar

* Bitcoin (BTC)
* Ethereum (ETH)
* Dogecoin (DOGE)
* Apple (AAPL)
* Tesla (TSLA)
* NVIDIA (NVDA)

---

## 🚀 Fase 1: Planificación y Configuración

### ✅ Reunión de Lanzamiento

* Presentar el plan del proyecto.
* Confirmar los 6 activos a analizar.
* Asignar equipos de trabajo.

**Estructura Sugerida (10 integrantes):**

* **Equipo de Liderazgo (2):** Gestión, GitHub, integración final.
* **Equipo Guía (4):** BTC y NVDA.
* **Equipo Cripto (3):** ETH, SOL, DOGE.
* **Equipo de Acciones (3):** AAPL, TSLA.

### ✅ Elección de Fuentes

* **Equipos Cripto:** API de CoinGecko.
* **Equipo Acciones:** Librería yfinance o API Alpha Vantage.
* Cada equipo revisa la documentación de su API.

### ✅ Configuración de GitHub

* Crear el repositorio.
* Invitar a todos los miembros.
* Proteger la rama principal (main).
* Subir archivos base:

  * `.gitignore`
  * `README.md` con estructura inicial.
  * `requirements.txt`.

---

## ⚙️ Fase 2: Desarrollo por Equipos

Cada equipo ejecutará estas tareas en paralelo.

### 1️⃣ Extracción de Datos

**a. Identificar Endpoint:**

* CoinGecko: `https://api.coingecko.com/api/v3/coins/{id}/market_chart`.
* Alpha Vantage: `TIME_SERIES_DAILY_ADJUSTED`.

**b. Claves de Autenticación:**

* CoinGecko: Sin clave básica.
* Alpha Vantage: API Key gratuita.

**c. Realizar Solicitud:**

* Usar `requests` con parámetros (`vs_currency=usd`, `days=365`).

**d. Procesar Respuesta:**

* Verificar `status_code`.
* Guardar JSON crudo.

**Resultado esperado:**

* `extraccion_{activo}.py`
* `datos_crudos_{activo}.json`

### 2️⃣ Limpieza y Procesamiento

**a. Cargar Datos:**

* Leer JSON con `pandas`.

**b. Explorar DataFrame:**

* `.head()`, `.info()`.

**c. Limpieza:**

* Seleccionar columnas relevantes.
* Manejar nulos.
* Convertir timestamps con `pd.to_datetime()`.
* Renombrar columnas a `Fecha` y `Precio_USD`.

**d. Guardar CSV limpio:**

* `datos_limpios_{activo}.csv`

### 3️⃣ Análisis y Visualización

**a. Cargar CSV limpio.**

**b. Análisis Descriptivo:**

* `.describe()`.

**c. Visualización preliminar:**

* Gráfico de línea simple.

**d. Validación interna:**

* Revisar que los datos sean correctos.

**Documentación:**

* El Equipo de Liderazgo completa secciones generales del `README.md`.
* Cada equipo redacta una breve descripción del activo.

---

## 🧩 Fase 3: Integración y Pruebas

### ✅ Integración de Módulos

* El Equipo de Liderazgo fusiona Pull Requests.
* Crear `analisis_final.py`:

  * Lee los 6 CSV.
  * Calcula rendimiento normalizado, volatilidad y correlación.

### ✅ Pruebas Funcionales

* Equipo de pruebas temporal ejecuta `analisis_final.py`.
* Verifica consistencia de resultados.

### ✅ Revisión y Depuración

* Reportar errores vía Issues en GitHub.
* Corregir en conjunto.

---

## 📝 Fase 4: Finalización y Entrega

### ✅ Documentación Final

* Redactar conclusiones del análisis comparativo.
* Incluir visualizaciones finales:

  * Gráfico de rendimiento normalizado.
  * Gráfico de volatilidad.
  * Mapa de calor de correlación.

### ✅ Preparación de Entregables

* Capturas del historial de commits.
* README.md completo.
* Versiones finales de gráficos.

### ✅ Revisión Final

* Verificar alineación con la rúbrica.
* Confirmar que todos los integrantes tengan contribución visible.

---

✅ **Escalabilidad:**

* *(*) Se puede agregar más activos o más métricas avanzadas de riesgo si hay tiempo.\*
