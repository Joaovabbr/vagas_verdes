import requests
import zipfile
import io
import os
from datetime import datetime
from .entities import LidarQuadrante
from .constants import (
    GEOSAMPA_DOWNLOAD_URL,
    LAZ_DOWNLOAD_PARAMS,
    GRID_MDT_PARAMS_STR,
    GRID_CACHE_PATH,
)

class SpLaz:
    """
    Cliente para acessar e baixar dados LIDAR do portal GeoSampa.
    Gerencia o download e cache da grade de articulação, além dos quadrantes específicos.
    """
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def ensure_grid_data(self) -> str:
        """Garante que a grade exista, baixando-a se necessário, e encontra o arquivo .shp."""
        download_necessario = False
        
        shp_files = list(GRID_CACHE_PATH.rglob("*.shp"))
        shp_path = shp_files[0] if shp_files else None

        if not shp_path:
            download_necessario = True
        else:
            try:
                response = self.session.head(f"{GEOSAMPA_DOWNLOAD_URL}?{GRID_MDT_PARAMS_STR}")
                if response.status_code == 200:
                    server_last_modified = response.headers.get('Last-Modified')
                    if server_last_modified:
                        local_time = datetime.fromtimestamp(os.path.getmtime(shp_path))
                        server_time = datetime.strptime(server_last_modified, '%a, %d %b %Y %H:%M:%S GMT')
                        if server_time > local_time:
                            download_necessario = True
            except Exception as e:
                print(f"Aviso: Não foi possível checar atualizações ({e}). Usando cache local.")

        if download_necessario:
            self._download_and_extract_grid()
            
            shp_files = list(GRID_CACHE_PATH.rglob("*.shp"))
            if not shp_files:
                raise FileNotFoundError("Nenhum arquivo .shp foi encontrado dentro do ZIP baixado.")
            shp_path = shp_files[0]

        return str(shp_path)
    
    def _download_and_extract_grid(self):
        print("Baixando grade de articulação...")
        response = self.session.get(GEOSAMPA_DOWNLOAD_URL, params=GRID_MDT_PARAMS_STR)
        response.raise_for_status()

        if not response.content.startswith(b'PK'):
            conteudo_texto = response.text[:200]
            raise ValueError(
                f"O GeoSampa não retornou um arquivo ZIP. Verifique os parâmetros.\n"
                f"Resposta do servidor: {conteudo_texto}"
            )

        os.makedirs(GRID_CACHE_PATH, exist_ok=True)
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(GRID_CACHE_PATH)
        print("Grade baixada e extraída com sucesso.")

    def download_quadrante(self, codigo_quadra: str) -> LidarQuadrante:
        """
        Baixa um quadrante LIDAR específico do GeoSampa.

        Args:
            codigo_quadra (str): Código do quadrante a ser baixado.

        Returns:
            LidarQuadrante: Objeto contendo os dados do quadrante baixado.
        """
        params = {
            "orig": LAZ_DOWNLOAD_PARAMS["orig"],
            "arq": f"{LAZ_DOWNLOAD_PARAMS['arq_prefix']}\\{codigo_quadra}.zip",
            "arqTipo": LAZ_DOWNLOAD_PARAMS["arq_tipo"]
        }

        response = self.session.get(GEOSAMPA_DOWNLOAD_URL, params=params)
        response.raise_for_status()

        return self._processar_zip(codigo_quadra, response.content)

    def _processar_zip(self, codigo: str, conteudo_zip: bytes) -> LidarQuadrante:
        try:
            with zipfile.ZipFile(io.BytesIO(conteudo_zip)) as z:
                nome_laz = z.namelist()[0]
                dados_laz = z.read(nome_laz)
                return LidarQuadrante(codigo, dados_laz, nome_laz)
        except zipfile.BadZipFile:
            raise ValueError(f"Conteudo baixado para o quadrante {codigo} invalido.")

    def download_lista(self, codigos: list) -> list:
        return [self.download_quadrante(c) for c in codigos]