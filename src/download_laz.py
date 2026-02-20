import requests
import os
import zipfile
import io

def download_laz_quadra(codigo_quadra: str, pasta_destino:str) -> None:
    url_download = f"https://download.geosampa.prefeitura.sp.gov.br/PaginasPublicas/downloadArquivo.aspx?orig=DownloadMapaArticulacao&arq=MDS_2020%5C{codigo_quadra}.zip&arqTipo=MAPA_ARTICULACAO"

    os.makedirs(pasta_destino, exist_ok=True)
    caminho_arquivo = os.path.join(pasta_destino, f"MDS_2020_{codigo_quadra}")

    response = requests.get(url_download)
    if response.status_code == 200:
        zip_virtual = io.BytesIO(response.content)

        with zipfile.ZipFile(zip_virtual) as zip:
            file_name = zip.namelist()[0]
            zip.extract(file_name, caminho_arquivo)
        
        print(f"Arquivo {file_name} extraído para {caminho_arquivo}")
    else:
        print(f"Erro ao baixar o arquivo: {response.status_code}")
        