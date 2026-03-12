import os
from pathlib import Path

CACHE_DIR = Path.home() / ".geosp_laz_api"
GRID_CACHE_PATH = CACHE_DIR / "articulacao_2020"
SHP_FILE_NAME = "SIRGAS_SHP_quadriculamdt.shp" 

GEOSAMPA_DOWNLOAD_URL = "https://download.geosampa.prefeitura.sp.gov.br/PaginasPublicas/downloadArquivo.aspx"

GRID_MDT_PARAMS_STR = "orig=DownloadCamadas&arq=21_Articulacao%20de%20Imagens%5C%5CArticula%E7%E3o%20MDT%5C%5CShapefile%5C%5CSIRGAS_SHP_quadriculamdt&arqTipo=Shapefile"

LAZ_DOWNLOAD_PARAMS = {
    "orig": "DownloadMapaArticulacao",
    "arq_prefix": "MDS_2020",
    "arq_tipo": "MAPA_ARTICULACAO"
}

EPSG_SAO_PAULO = 31983