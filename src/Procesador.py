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
   def transformar_a_dataframe(self) -> pd.DataFrame:
        """APORTE INTEGRANTE 4: transforma el GeoJSON de la API en un DataFrame limpio."""
        if not self.datos or "features" not in self.datos:
            print("[ERROR] No hay datos válidos para procesar.")
            return pd.DataFrame()

        registros = []
        for sismo in self.datos["features"]:
            props = sismo.get("properties", {})
            geometria = sismo.get("geometry", {})
            coords = geometria.get("coordinates", [None, None, None])

            lugar_texto = props.get("place", "")
            distancia_km, direccion, ciudad = self.extraer_info_lugar(lugar_texto)

            registros.append({
                "Fecha": pd.to_datetime(props.get("time"), unit="ms", errors="coerce"),
                "Magnitud": props.get("mag"),
                "Lugar": lugar_texto,
                "Ciudad_Referencia": ciudad,
                "Distancia_km": distancia_km,
                "Direccion": direccion,
                "Profundidad_km": coords[2],
                "Latitud": coords[1],
                "Longitud": coords[0],
            })

        df = pd.DataFrame(registros)
        df = df.dropna(subset=["Magnitud", "Profundidad_km"])

        df["Nivel"] = pd.cut(
            df["Magnitud"],
            bins=[0, 3.9, 4.9, 5.9, 10],
            labels=["Leve", "Moderado", "Fuerte", "Muy Fuerte"],
        )

        df = df.sort_values(by="Fecha", ascending=False).reset_index(drop=True)
        self.df_limpio = df
        return self.df_limpio

procesador = ProcesadorSismos(datos_crudos)
df_final = procesador.transformar_a_dataframe()
df_final.head(10)
