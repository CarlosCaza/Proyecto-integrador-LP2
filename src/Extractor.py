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

    # Coordenadas aproximadas que encierran todo el territorio peruano
    LAT_MIN, LAT_MAX = -18.5, -0.0
    LON_MIN, LON_MAX = -81.5, -68.5

    def __init__(self, dias_atras: int = 90, magnitud_minima: float = 2.5):
        self.url_base = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        self.dias_atras = dias_atras
        self.magnitud_minima = magnitud_minima
        self.datos_brutos = None

    def conectar_y_descargar(self) -> dict:
        """Realiza una solicitud HTTP GET a la API del USGS y descarga los sismos en Perú."""
        fecha_fin = datetime.utcnow()
        fecha_inicio = fecha_fin - timedelta(days=self.dias_atras)

        parametros = {
            "format": "geojson",
            "starttime": fecha_inicio.strftime("%Y-%m-%d"),
            "endtime": fecha_fin.strftime("%Y-%m-%d"),
            "minlatitude": self.LAT_MIN,
            "maxlatitude": self.LAT_MAX,
            "minlongitude": self.LON_MIN,
            "maxlongitude": self.LON_MAX,
            "minmagnitude": self.magnitud_minima,
            "orderby": "time",
        }

        try:
            print(f"[INFO] Conectando a la red: {self.url_base}")
            respuesta = requests.get(self.url_base, params=parametros, timeout=15)

            if respuesta.status_code == 200:
                self.datos_brutos = respuesta.json()
                total = len(self.datos_brutos.get("features", []))
                print(f"[INFO] Datos descargados correctamente. Sismos encontrados: {total}")
                return self.datos_brutos
            else:
                print(f"[ERROR] Código de estado HTTP inesperado: {respuesta.status_code}")
                return {}
        except requests.exceptions.RequestException as e:
            print(f"[CRÍTICO] Fallo en la conexión de red: {e}")
            return {}
