import os
import io
from google.cloud import vision
from utils import dump_env_json_to_file

def ler_imagem(file_path):
    # Garante que a credencial está salva e pega o path
    cred_path = dump_env_json_to_file("GOOGLE_CLOUD_CREDENTIALS", "google_cloud.json")
    client = vision.ImageAnnotatorClient.from_service_account_file(cred_path)
    with io.open(file_path, 'rb') as f:
        content = f.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    return response.text_annotations[0].description if response.text_annotations else ""

def extrair_valor(texto):
    import re
    # Busca valores em formato 120.90 ou 120,90
    valores = re.findall(r"\d+[.,]\d{2}", texto)
    if valores:
        v = valores[0].replace(",", ".")
        try:
            return float(v)
        except:
            return None
    return None
