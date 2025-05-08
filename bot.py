import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from db import cadastrar_usuario, adicionar_gasto, buscar_gastos, usuario_ativo
from sheets import criar_planilha_usuario, adicionar_gasto_sheet
from ocr import ler_imagem, extrair_valor

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    nome = update.effective_user.full_name
    url = criar_planilha_usuario(user_id)
    cadastrar_usuario(user_id, nome, url)
    await update.message.reply_text(f"Bem-vindo! Sua planilha: {url}")

async def despesa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not usuario_ativo(update.effective_user.id):
        await update.message.reply_text("Assinatura inativa. Renove para continuar usando!")
        return
    try:
        _, valor, descricao, categoria = update.message.text.split(maxsplit=3)
        gasto = {"data": "2025-05-09", "descricao": descricao, "valor": float(valor), "categoria": categoria}
        adicionar_gasto(update.effective_user.id, gasto)
        adicionar_gasto_sheet(update.effective_user.id, gasto)
        await update.message.reply_text("Despesa registrada!")
    except Exception as e:
        await update.message.reply_text("Formato: /despesa valor descrição categoria")

async def resumo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not usuario_ativo(update.effective_user.id):
        await update.message.reply_text("Assinatura inativa. Renove para continuar usando!")
        return
    gastos = buscar_gastos(update.effective_user.id)
    if not gastos:
        await update.message.reply_text("Nenhuma despesa registrada.")
        return
    soma = sum([g['valor'] for g in gastos if 'valor' in g])
    await update.message.reply_text(f"Total lançado: R${soma:.2f}")

async def receber_recibo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not usuario_ativo(update.effective_user.id):
        await update.message.reply_text("Assinatura inativa!")
        return
    if update.message.photo:
        file = await update.message.photo[-1].get_file()
        file_path = f"recibo_{update.effective_user.id}.jpg"
        await file.download_to_drive(custom_path=file_path)
        texto_extraido = ler_imagem(file_path)
        valor = extrair_valor(texto_extraido)
        if valor:
            gasto = {"data": "2025-05-09", "descricao": "Recibo OCR", "valor": valor, "categoria": "Automático"}
            adicionar_gasto(update.effective_user.id, gasto)
            adicionar_gasto_sheet(update.effective_user.id, gasto)
            await update.message.reply_text(f"Despesa de R${valor:.2f} registrada via recibo!")
        else:
            await update.message.reply_text("Não consegui identificar valor no recibo.")
    else:
        await update.message.reply_text("Envie uma foto do recibo.")

application = Application.builder().token(os.environ["TELEGRAM_TOKEN"]).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("despesa", despesa))
application.add_handler(CommandHandler("resumo", resumo))
application.add_handler(MessageHandler(filters.PHOTO, receber_recibo))

from scheduler import iniciar_agendamento
iniciar_agendamento(application)

application.run_polling()
