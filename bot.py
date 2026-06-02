import os
import logging
import requests
import pytesseract
from urllib.parse import quote
from PIL import Image
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
HF_API_KEY = os.getenv("HF_API_KEY")

logging.basicConfig(level=logging.INFO)

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
os.environ["TESSDATA_PREFIX"] = (
    r"C:\Program Files\Tesseract-OCR\tessdata"
)

guardian_map = {}


def heuristic_analysis(text):
    text_lower = text.lower()

    red_flags = [
        "urgente",
        "fraude nas urnas",
        "compartilhe antes que apaguem",
        "pix",
        "senha",
        "cpf bloqueado",
        "clique aqui",
        "atualize seus dados",
        "conta bloqueada",
        "acesso incomum",
        "intervenção militar",
        "governo esconde",
    ]

    score = sum(flag in text_lower for flag in red_flags)

    reasons = []

    if score >= 3:
        reasons.append("múltiplos sinais suspeitos")

    if text.count("!") >= 3:
        reasons.append("excesso de exclamações")

    uppercase_ratio = sum(
        1 for c in text if c.isupper()
    ) / max(len(text), 1)

    if uppercase_ratio > 0.3:
        reasons.append("uso excessivo de caixa alta")

    return score, reasons


def analyze_with_hf(text):
    API_URL = (
        "https://api-inference.huggingface.co/models/"
        "facebook/bart-large-mnli"
    )

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }

    payload = {
        "inputs": text,
        "parameters": {
            "candidate_labels": [
                "golpe digital",
                "fake news política",
                "notícia legítima",
            ]
        }
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        result = response.json()

        label = result["labels"][0]
        score = result["scores"][0]

        return label, score

    except Exception:
        return None, 0


def verificar_fact_check(texto):
    query = quote(texto[:120])

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    sites = [
        "site:lupa.uol.com.br",
        "site:aosfatos.org",
        "site:projetocomprova.com.br",
    ]

    for site in sites:
        url = f"https://www.google.com/search?q={site}+{query}"

        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=10
            )

            html = response.text.lower()

            if (
                "nenhum documento encontrado" not in html
                and "did not match any documents" not in html
            ):
                return True

        except Exception:
            continue

    return False


def final_analysis(text):
    heuristic_score, reasons = heuristic_analysis(text)

    hf_label, hf_score = analyze_with_hf(text)

    fact_check_found = verificar_fact_check(text)

    final_result = "🟢 BAIXO RISCO"

    if heuristic_score >= 3:
        final_result = "🔴 POSSÍVEL GOLPE / FAKE NEWS"

    if hf_label in ["golpe digital", "fake news política"] and hf_score > 0.6:
        final_result = "🔴 POSSÍVEL GOLPE / FAKE NEWS"
        reasons.append(f"IA detectou: {hf_label}")

    if fact_check_found:
        final_result = "🔴 POSSÍVEL GOLPE / FAKE NEWS"
        reasons.append("verificação encontrada em agência de fact-check")

    if final_result == "🟢 BAIXO RISCO" and heuristic_score >= 1:
        final_result = "🟡 CONTEÚDO SUSPEITO"

    return final_result, reasons


async def process_analysis(update, context, text):
    result, reasons = final_analysis(text)

    reasons_text = "\n".join(
        [f"• {reason}" for reason in reasons]
    ) or "• nenhum sinal crítico detectado"

    resposta = (
        f"{result}\n\n"
        f"Motivos:\n{reasons_text}"
    )

    await update.message.reply_text(resposta)

    if result.startswith("🔴"):
        user_id = update.effective_user.id

        if user_id in guardian_map:
            guardian_id = guardian_map[user_id]

            await context.bot.send_message(
                chat_id=guardian_id,
                text="🚨 ALERTA: possível golpe ou fake news detectado."
            )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Envie texto ou imagem para análise."
    )


async def meu_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Seu ID: {update.effective_user.id}"
    )


async def anjo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text(
            "Use: /anjo ID_DO_FAMILIAR"
        )
        return

    guardian_map[update.effective_user.id] = context.args[0]

    await update.message.reply_text(
        "Anjo da Guarda cadastrado."
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await process_analysis(
        update,
        context,
        update.message.text
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()

    file_path = "temp.jpg"
    await file.download_to_drive(file_path)

    text = pytesseract.image_to_string(
        Image.open(file_path),
        lang="por"
    )

    await process_analysis(update, context, text)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("meu_id", meu_id))
    app.add_handler(CommandHandler("anjo", anjo))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)
    )
    app.add_handler(
        MessageHandler(filters.PHOTO, handle_photo)
    )

    app.run_polling()


if __name__ == "__main__":
    main()