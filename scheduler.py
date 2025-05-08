from apscheduler.schedulers.background import BackgroundScheduler
import pytz
from db import get_firestore

def enviar_lembretes(app):
    db = get_firestore()
    users = db.collection("users").where("assinatura_status", "==", "ativo").stream()
    for u in users:
        app.bot.send_message(
            chat_id=u.id, 
            text="Já registrou suas despesas de hoje? Use /despesa para não perder o controle!"
        )

def iniciar_agendamento(app):
    scheduler = BackgroundScheduler(timezone=pytz.timezone("America/Sao_Paulo"))
    scheduler.add_job(lambda: enviar_lembretes(app), 'cron', hour=20, minute=0)
    scheduler.start()
