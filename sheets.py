import os
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

def get_cred():
    cred_path = "/tmp/sa_google.json"
    # Só cria o arquivo se não existir ainda
    if not os.path.exists(cred_path):
        with open(cred_path, "w") as f:
            f.write(os.environ["GOOGLE_CLOUD_CREDENTIALS"])
    from google.oauth2.service_account import Credentials
    return Credentials.from_service_account_file(cred_path)
    
def criar_planilha_usuario(telegram_id):
    creds = get_cred()
    client = gspread.authorize(creds)
    nova = client.copy(
        os.environ['GOOGLE_SHEETS_TEMPLATE_ID'],
        title=f"Finanças_{telegram_id}",
        copy_permissions=True
    )
    url = f'https://docs.google.com/spreadsheets/d/{nova.id}/edit'
    return url

def adicionar_gasto_sheet(telegram_id, gasto):
    creds = get_cred()
    client = gspread.authorize(creds)
    planilha = client.open(f"Finanças_{telegram_id}")
    ws = planilha.sheet1
    # [{data}, {desc}, {valor}, {categoria}]
    ws.append_row([
        gasto['data'] if 'data' in gasto else datetime.today().strftime("%d/%m/%Y"),
        gasto['descricao'],
        gasto['valor'],
        gasto['categoria']
    ])
