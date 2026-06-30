# APORTE INTEGRANTE 4: Clase ProcesadorSismos (incluye el metodo regex del Integrante 3)
class ProcesadorSismos:
    """Clase encargada de limpiar, validar y transformar los datos de sismos."""

    def __init__(self, datos_api: dict):
        self.datos = datos_api
        self.df_limpio = None

    def extraer_info_lugar(self, texto_lugar: str):
        """
        APORTE INTEGRANTE 3: usa regex para extraer (distancia_km, direccion, ciudad)
        del texto del lugar del sismo.
        """
        coincidencia = re.match(PATRON_LUGAR, texto_lugar.strip())
        if coincidencia:
            distancia_km = int(coincidencia.group(1))
            direccion = coincidencia.group(2)
            ciudad = coincidencia.group(3).strip()
            return distancia_km, direccion, ciudad
        else:
            return None, None, texto_lugar.strip()
