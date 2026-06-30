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
