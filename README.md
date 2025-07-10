# Trabajo-Encargado-LP2
Repositorio del Trabajo Encargado LP2 con Chalán

```mermaid
graph TD
    classDef fase fill:#2a9d8f,stroke:#264653,stroke-width:2px,color:#fff,font-weight:bold
    classDef equipo fill:#e9c46a,stroke:#264653,stroke-width:2px,color:#264653
    classDef tarea fill:#f4a261,stroke:#264653,stroke-width:1px,color:#264653
    classDef integracion fill:#e76f51,stroke:#264653,stroke-width:2px,color:#fff
    classDef inicio_fin fill:#264653,stroke:#fff,stroke-width:2px,color:#fff,font-weight:bold

    A["Inicio del Proyecto"]:::inicio_fin
    B("Fase 1: Planificación y Configuración"):::fase
    B1["1- Reunión de Lanzamiento<br>2- Elección de Fuentes<br>3- Configuración de GitHub"]:::tarea
    
    A --> B --> B1

    C("Fase 2: Desarrollo por Equipos"):::fase
    B1 --> C

    subgraph "Equipo 1 (BTC, SP500)"
        direction TB
        E1_1("Extracción de Datos<br>BTC, SP500"):::equipo
        E1_2("Limpieza y Procesamiento"):::equipo
        E1_3("Análisis y Visualización"):::equipo
        E1_1 --> E1_2 --> E1_3
    end

    subgraph "Equipo 2 (ETH, DOGE)"
        direction TB
        E2_1("Extracción de Datos<br>ETH, DOGE"):::equipo
        E2_2("Limpieza y Procesamiento"):::equipo
        E2_3("Análisis y Visualización"):::equipo
        E2_1 --> E2_2 --> E2_3
    end

    subgraph "Equipo 3 (AAPL, TSLA, NVDA)"
        direction TB
        E3_1("Extracción de Datos<br>AAPL, TSLA, NVDA"):::equipo
        E3_2("Limpieza y Procesamiento"):::equipo
        E3_3("Análisis y Visualización"):::equipo
        E3_1 --> E3_2 --> E3_3
    end

    C --> E1_1
    C --> E2_1
    C --> E3_1

    D("Fase 3: Integración y Pruebas"):::integracion
    D1["1- Integración de Módulos (Pull Requests)<br>2- Pruebas Funcionales<br>3- Revisión y Depuración"]:::tarea

    E1_3 --> D
    E2_3 --> D
    E3_3 --> D
    D --> D1

    E("Fase 4: Finalización y Entrega"):::fase
    E1["1- Documentación Final<br>2- Preparación de Entregables<br>3- Revisión Final"]:::tarea
    D1 --> E --> E1

    F["Fin del Proyecto"]:::inicio_fin
    E1 --> F

```


# Título del Proyecto

## 🎯 Objetivo
Este proyecto busca analizar ...

## 🛠️ APIs Utilizadas
* API1
* API2

## 🚀 Instrucciones de Uso
1.  Clonar el repositorio.
2.  Instalar las dependencias: `pip install -r requirements.txt`
3.  Ejecutar el script principal: `python main.py`

## 📊 Visualizaciones
*Aquí se insertarán los gráficos y tablas finales.*

# Integrantes
| Integrante | Código | Usuario |
|---|---|---|
| Vargas Maldonado, Bryan | 20230535 | Bryared |
| Vargas Maldonado, Andrew | 20240959 | andrwxl |
| Villanueva Huamani Alexander | 20230419 | ... |
| Alva Aquino Nicole | 20221388 | ... |
| Ruiz Macedo Fernando Jose | 20211830 | ... |
| Ramos Correa, Freddy | 20230408 | ... |
| Coronado de la vega, Alonso| 20221395 | ron-62 |
| Lopez Acuña Victor Andreé | 20180206 | VictorLopez281199 |
| Arroyo Arruz, Alejandra  | 20211805 | Alejandra-1805 |
| Nombre Alumno 10 | C010 |
| Nombre Alumno 11 | C011 |
