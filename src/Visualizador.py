# VISUALIZACION Y REPORTE ESTADISTICO

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class VisualizadorSismos:
  """Clase encargadad de la generacion de reportes visuales sobre lossismos en el Perú."""
  def __init__(self, dataframe: pd.Dataframe):
    self.df = dataframe

  def grafico_barras_por_nivel(self):
    """Grafico 1: Cantidad de sismos registrados según su nivel de intensidad."""
    plt.figure(figsize=(8, 5))
    orden = ["Leve", "Moderado", "Fuerte", "Muy Fuerte"]
    sns.countplot(x="Nivel", data=self.df, order=orden, palette="Reds")
    plt.title("Gráfico 1: Cantidad de Sismos por Nivel de Intensidad (Perú)")
    plt.xlabel("Nivel de Intensidad")
    plt.ylabel("Cantidad de Sismos")
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()
