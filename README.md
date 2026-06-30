# Sismos en Perú — Proyecto Integrador (Lenguaje de Programación II)

## Objetivo
Analizar la actividad sísmica reciente en el territorio peruano usando datos reales
y actualizados de la API pública del **USGS (United States Geological Survey)**,
aplicando Programación Orientada a Objetos, programas en red, expresiones
regulares, procesamiento con pandas y visualización de datos.

## Fuente de datos
API pública y gratuita del USGS (no requiere API key ni registro):
`https://earthquake.usgs.gov/fdsnws/event/1/query`

Se consultan los sismos de los últimos 90 días dentro de las coordenadas que
cubren el territorio peruano, con magnitud mínima de 2.5.

## Estructura del proyecto
```
proyecto/
├── main.py                 # Orquestación general (LUIS Y JAVIER)
├── requirements.txt        # Dependencias del proyecto
├── README.md
└── src/
    ├── extractor.py         # Clase ExtractorSismos (JOEL - red/API)
    ├── procesador.py        # Clase ProcesadorSismos (DANTE - regex, JORGE - pandas)
    └── visualizador.py       # Clase VisualizadorSismos (CARLOS - gráficos)
```

## Integrantes y aportes
| # | Integrante | Aporte |
|---|------------|--------|
| 1 | LUIS | Configuración inicial y orquestación del flujo (`main.py`) |
| 2 | JOEL | Conexión de red y consumo de la API (`src/extractor.py`) |
| 3 | DANTE | Validación/extracción con expresiones regulares (`src/procesador.py`) |
| 4 | JORGE | Procesamiento y limpieza con pandas (`src/procesador.py`) |
| 5 | CARLOS | Visualización de datos (`src/visualizador.py`) |
| 6 | JAVIER | Integración final y resumen de resultados (`main.py`) |

## Instalación
```bash
git clone <url-del-repositorio>
cd proyecto
pip install -r requirements.txt
```

## Ejecución
```bash
python main.py
```

## Resultados
El programa descarga los sismos recientes en Perú, los limpia y clasifica por
nivel de intensidad (Leve, Moderado, Fuerte, Muy Fuerte), y genera 3 gráficos:
1. Cantidad de sismos por nivel de intensidad (barras).
2. Evolución de la magnitud en el tiempo (líneas).
3. Dispersión de la profundidad de los sismos (boxplot).

Finalmente muestra un resumen estadístico: total de sismos, magnitud
promedio, sismo más fuerte y profundidad promedio.
