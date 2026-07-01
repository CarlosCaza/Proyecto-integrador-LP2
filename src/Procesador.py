import re
import pandas as pd

class ProcesadorSismos:
    """Clase encargada de limpiar, validar y transformar los datos de sismos."""

    # CORRECCIÓN DANTE: Cambiado a {1,3} para capturar direcciones como ESE o ENE
    PATRON_LUGAR = r"(\d+)\s*km\s+([NSEW]{1,3})\s+of\s+([A-Za-zà-ÿ\s]+),\s*Peru"

    def __init__(self, datos_api: dict):
        self.datos = datos_api
        self.df_limpio = None

    def extraer_info_lugar(self, texto_lugar: str):
        """
        Extrae la distancia, dirección y ciudad de un texto de lugar.
        """
        if not isinstance(texto_lugar, str):
            return None, None, "Desconocido"
            
        coincidencia = re.match(self.PATRON_LUGAR, texto_lugar.strip())
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

        # Generación de la columna 'Nivel' requerida por el visualizador
        df["Nivel"] = pd.cut(
            df["Magnitud"],
            bins=[0, 3.9, 4.9, 5.9, 10],
            labels=["Leve", "Moderado", "Fuerte", "Muy Fuerte"],
        )

        df = df.sort_values(by="Fecha", ascending=False).reset_index(drop=True)
        self.df_limpio = df

        # Redondeo de variables numéricas para mejorar la presentación visual
        df["Profundidad_km"] = df["Profundidad_km"].round(2)
        df["Latitud"] = df["Latitud"].round(4)
        df["Longitud"] = df["Longitud"].round(4)



        return self.df_limpio

# PROTECCIÓN: Evita la ejecución automática de código suelto al ser importado por main.py
if __name__ == "__main__":
    print("[INFO] Clase ProcesadorSismos cargada correctamente en modo local.")
