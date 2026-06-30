# CONFIGURACIÓN INICIAL Y ORQUESTACIÓN

from src.extractor import ExtractorSismos
from src.procesador import ProcesadorSismos
from src.visualizador import VisualizadorSismos

print("=" * 60)
print(" PROYECTO INTEGRADOR: SISMOS EN PERÚ (Fuente: API USGS) ")
print("=" * 60)

print("\n Configuración inicial")
DIAS_A_CONSULTAR = 90
MAGNITUD_MINIMA = 2.5
print(f"    Consultando sismos de los últimos {DIAS_A_CONSULTAR} días, "
      f"magnitud >= {MAGNITUD_MINIMA}")


