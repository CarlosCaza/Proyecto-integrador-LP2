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

extractor = ExtractorSismos(dias_atras=DIAS_A_CONSULTAR, magnitud_minima=MAGNITUD_MINIMA)
datos_crudos = extractor.conectar_y_descargar()

print("\n Extracción de datos vía API (red)")
print("    (ver src/extractor.py para el detalle de la solicitud HTTP)")


print("\n Procesamiento")
procesador = ProcesadorSismos(datos_crudos)
df_final = procesador.transformar_a_dataframe()
print("    Muestra de datos procesados:")
print(df_final.head())


print("\n Generación de gráficos")
visualizador = VisualizadorSismos(df_final)
visualizador.grafico_barras_por_nivel()
visualizador.grafico_lineas_magnitud_tiempo()
visualizador.grafico_caja_profundidad()
