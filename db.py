import os
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials
from utils import dump_env_json_to_file  # idêntico ao acima

def inicializar_firebase():
    cred_path = dump_env_json_to_file("FIREBASE_CREDENTIALS", "firebase.json")
    cred = credentials.Certificate(cred_path)
    # Só inicializa uma vez!
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

def get_firestore():
    cred_path = os.environ["FIREBASE_CREDENTIALS"]
    return firestore.Client.from_service_account_json(cred_path)

def cadastrar_usuario(telegram_id, nome, planilha_url):
    db = get_firestore()
    db.collection("users").document(str(telegram_id)).set({
        "nome": nome,
        "planilha_url": planilha_url,
        "assinatura_status": "ativo"
    })

def adicionar_gasto(telegram_id, gasto):
    db = get_firestore()
    gastos_ref = db.collection("users").document(str(telegram_id)).collection("gastos")
    gastos_ref.add(gasto)

def buscar_gastos(telegram_id):
    db = get_firestore()
    gastos_ref = db.collection("users").document(str(telegram_id)).collection("gastos").stream()
    return [g.to_dict() for g in gastos_ref]

def usuario_ativo(telegram_id):
    db = get_firestore()
    doc = db.collection("users").document(str(telegram_id)).get()
    return doc.exists and doc.to_dict().get("assinatura_status") == "ativo"
