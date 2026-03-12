"""
splaz: Uma biblioteca para facilitar o acesso e geocodificação 
de dados LiDAR (MDS/MDT) do portal GeoSampa da cidade de São Paulo.
"""

from .entities import LidarQuadrante
from .downloader import SpLaz
from .geocoder import SpLazGeo

__all__ = [
    "LidarQuadrante",
    "SpLaz",
    "SpLazGeo",
]

__version__ = "0.1.0"
__author__ = "João Braga"