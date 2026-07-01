# CONFIGURACIÓN INICIAL Y ORQUESTACIÓN

from src.Extractor import ExtractorSismos
from src.Procesador import ProcesadorSismos
from src.Visualizador import VisualizadorSismos

print(" PROYECTO INTEGRADOR: SISMOS EN PERÚ (Fuente: API USGS) ")

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

# INTEGRACIÓN FINAL Y RESULTADOS

print("\n Resumen final del análisis")
if not df_final.empty:
    print(f"    Total de sismos analizados: {len(df_final)}")
    print(f"    Magnitud promedio: {df_final['Magnitud'].mean():.2f}")
    print(f"    Sismo más fuerte: {df_final['Magnitud'].max():.2f} "
          f"({df_final.loc[df_final['Magnitud'].idxmax(), 'Lugar']})")
    print(f"    Profundidad promedio: {df_final['Profundidad_km'].mean():.1f} km")
    print("\n    Conclusión: estos datos confirman que Perú, al estar en el")
    print("    Cinturón de Fuego del Pacífico, registra actividad sísmica")
    print("    constante, mayormente de intensidad leve a moderada.")
else:
    print("    No se pudo generar el resumen porque no llegaron datos de la API.")

print(" FIN DEL ANÁLISIS ")
