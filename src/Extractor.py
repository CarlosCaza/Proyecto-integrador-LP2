# ============================================================
# CONEXIÓN DE RED Y SOLICITUDES HTTP (API)
# ============================================================
#
# Qué hace esta parte:
# - Se conecta a la API pública del USGS (Servicio Geológico de EE.UU.)
# - Esta API es 100% gratuita, NO requiere API key, NO tiene límites
#   estrictos de uso, y entrega datos REALES y ACTUALIZADOS de sismos
#   ocurridos en cualquier parte del mundo, en formato GeoJSON.
# - Filtramos los sismos solo dentro del territorio peruano usando
#   un "bounding box" (rectángulo de coordenadas que cubre Perú).
# - Aquí se cumple el requisito de "Programas en red": usamos la
#   librería requests para hacer una solicitud HTTP GET real.

import requests
from datetime import datetime, timedelta

class ExtractorSismos:
    """Clase encargada de la conexión de red y obtención de datos de sismos en Perú."""

    # Atributos de clase: Definen el "bounding box" (caja delimitadora) para filtrar 
    # únicamente los sismos que caen dentro del área geográfica de Perú.
    LAT_MIN, LAT_MAX = -18.5, -0.0
    LON_MIN, LON_MAX = -81.5, -68.5

    def __init__(self, dias_atras: int = 90, magnitud_minima: float = 2.5):
        # El constructor inicializa los parámetros clave de la búsqueda.
        # Por defecto, buscará sismos de los últimos 90 días con magnitud mayor a 2.5.
        self.url_base = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        self.dias_atras = dias_atras
        self.magnitud_minima = magnitud_minima
        self.datos_brutos = None

    def conectar_y_descargar(self) -> dict:
        """Realiza una solicitud HTTP GET a la API del USGS y descarga los sismos en Perú."""
        
        # 1. CÁLCULO DE FECHAS: La API necesita una fecha de inicio y fin.
        # Calculamos la fecha de inicio restando los 'dias_atras' a la fecha actual (UTC).
        fecha_fin = datetime.utcnow()
        fecha_inicio = fecha_fin - timedelta(days=self.dias_atras)

        # 2. CONSTRUCCIÓN DE PARÁMETROS: Diccionario que requests convertirá en la 
        # cadena de consulta (query string) en la URL (ej. ?format=geojson&starttime=...).
        parametros = {
            "format": "geojson", # Formato de respuesta deseado
            "starttime": fecha_inicio.strftime("%Y-%m-%d"), # Fecha inicial formateada
            "endtime": fecha_fin.strftime("%Y-%m-%d"),      # Fecha final formateada
            "minlatitude": self.LAT_MIN,   # Filtro geográfico Sur
            "maxlatitude": self.LAT_MAX,   # Filtro geográfico Norte
            "minlongitude": self.LON_MIN,  # Filtro geográfico Oeste
            "maxlongitude": self.LON_MAX,  # Filtro geográfico Este
            "minmagnitude": self.magnitud_minima, # Filtro de intensidad
            "orderby": "time",             # Ordenar del más reciente al más antiguo
        }

        # 3. CONEXIÓN Y DESCARGA: Se usa un bloque try-except para evitar que el 
        # programa colapse si no hay internet o la API está caída.
        try:
            print(f"[INFO] Conectando a la red: {self.url_base}")
            # Realiza la petición GET enviando los parámetros. El 'timeout' evita 
            # que el código se quede colgado indefinidamente si el servidor no responde.
            respuesta = requests.get(self.url_base, params=parametros, timeout=15)

            # 4. VALIDACIÓN DE RESPUESTA: El código 200 indica que la petición fue exitosa ("OK").
            if respuesta.status_code == 200:
                # Convierte la respuesta de texto (JSON) a un diccionario de Python.
                self.datos_brutos = respuesta.json()
                
                # Extrae la lista de sismos (features). Si no hay, devuelve una lista vacía [].
                total = len(self.datos_brutos.get("features", []))
                
                print(f"[INFO] Datos descargados correctamente. Sismos encontrados: {total}")
                return self.datos_brutos
            else:
                # Si devuelve 404 (No encontrado), 500 (Error de servidor), etc.
                print(f"[ERROR] Código de estado HTTP inesperado: {respuesta.status_code}")
                return {}
                
        except requests.exceptions.RequestException as e:
            # Captura cualquier error relacionado con la red (sin internet, timeout, etc.)
            print(f"[CRÍTICO] Fallo en la conexión de red: {e}")
            return {}
