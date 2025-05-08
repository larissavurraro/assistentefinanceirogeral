import os
from google.cloud import firestore

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
