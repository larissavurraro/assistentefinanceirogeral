import os
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from utils import dump_env_json_to_file  # Certifique-se que utils.py está correto!

def get_cred():
    cred_path = dump_env_json_to_file("GOOGLE_CLOUD_CREDENTIALS", "sa_google.json")
    return Credentials.from_service_account_file(cred_path)

def criar_planilha_usuario(telegram_id):
    creds = get_cred()
    client = gspread.authorize(creds)
    nova = client.copy(
        os.environ['GOOGLE_SHEETS_TEMPLATE_ID'],
        title=f"Financas_{telegram_id}",
        copy_permissions=True
    )
    url = f'https://docs.google.com/spreadsheets/d/{nova.id}/edit'
    return url

def adicionar_gasto_sheet(telegram_id, gasto):
    creds = get_cred()
    client = gspread.authorize(creds)
    planilha = client.open(f"Financas_{telegram_id}")
    ws = planilha.sheet1
    ws.append_row([
        gasto['data'] if 'data' in gasto else datetime.today().strftime("%d/%m/%Y"),
        gasto['descricao'],
        gasto['valor'],
        gasto['categoria']
    ])
