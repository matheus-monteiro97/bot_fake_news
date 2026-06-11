import os
import logging
import requests
import pytesseract
import re

from dotenv import load_dotenv
from PIL import Image

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from analysis.heuristics import analyze_heuristics
from analysis.fake_score import (
    calculate_fake_score,
    classify_score
)
from analysis.fact_check import fact_check
from analysis.explanation import generate_explanation
from database.db import (
    init_db,
    save_analysis
)

from analysis.url_analysis import (
    extract_text_from_url
)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
HF_API_KEY = os.getenv("HF_API_KEY")

logging.basicConfig(level=logging.INFO)

# caminho do tesseract
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

os.environ["TESSDATA_PREFIX"] = (
    r"C:\Program Files\Tesseract-OCR\tessdata"
)

guardian_map = {}

def extract_urls(text):

    pattern = r"https?://[^\s]+"

    return re.findall(
        pattern,
        text
    )
def analyze_with_hf(text):

    API_URL = (
        "https://router.huggingface.co/hf-inference/models/"
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
                "notícia legítima"
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

        print("Status:", response.status_code)

        result = response.json()

        print("Resultado bruto:")
        print(result)

        if "labels" in result:

            label = result["labels"][0]
            score = result["scores"][0]

        return label, score
    except Exception as e:

        print("Erro:", e)

        return (
            "indefinido",
            0
        )

def final_analysis(text):

    # heurísticas
    heuristic_score, reasons = analyze_heuristics(text)

    # modelo HF
    hf_label, hf_score = analyze_with_hf(text)

    if hf_label is None:
        hf_label = "indefinido"
        hf_score = 0

    if (
        hf_label in [
            "golpe digital",
            "fake news política"
        ]
        and hf_score > 0.60
    ):
        reasons.append(
            f"IA detectou: {hf_label}"
        )

    # busca em agências
    fact_check_found, suspicious_score, fact_check_sources, corroborated_sources = fact_check(text)

    sources = (
        fact_check_sources +
        corroborated_sources
    )

    if fact_check_found:

        reasons.append(
            "Verificação encontrada em agência de fact-check"
        )

    elif len(corroborated_sources) >= 2:

        reasons.append(
            "Informação corroborada por múltiplas fontes"
        )

    # score final
    score = calculate_fake_score(
        heuristic_score=heuristic_score,
        hf_score=hf_score,
        fact_check_found=fact_check_found,
        corroborated_count=len(corroborated_sources)
    )

    category = classify_score(score)

    explanation = generate_explanation(
        text,
        reasons,
        sources
    )

    return {
        "score": score,
        "categoria": category,
        "motivos": reasons,
        "fontes": sources,
        "explicacao": explanation,
        "confianca_modelo": round(
            hf_score * 100,
            2
        )
    }

async def process_analysis(
        update,
        context,
        text):

    status_message = await update.message.reply_text(
        "🔍 Analisando conteúdo...\nIsso pode levar alguns segundos."
    )

    result = final_analysis(text)

    score = result["score"]

    categoria = result["categoria"]

    motivos = result["motivos"]

    explicacao = result["explicacao"]

    fontes = result["fontes"]

    motivos_text = ""

    if motivos:

        for motivo in motivos:

            motivos_text += f"✓ {motivo}\n"

    else:

        motivos_text = (
            "✓ Nenhum sinal crítico encontrado\n"
        )

    # Define cor e mensagem de alerta conforme a classificação
    emoji = "🟢"

    alerta = (
        "✅ Nenhum sinal crítico foi encontrado.\n\n"
    )

    if categoria == "MUITO PROVÁVEL SER FALSO":

        emoji = "🔴"

        alerta = (
            "⚠️ CUIDADO!\n"
            "Há fortes indícios de golpe ou desinformação.\n"
            "Não clique em links, não faça pagamentos e verifique a informação em fontes confiáveis.\n\n"
        )

    elif categoria == "PARCIALMENTE FALSO":

        emoji = "🟠"

        alerta = (
            "⚠️ ATENÇÃO!\n"
            "O conteúdo mistura informações verdadeiras e falsas.\n"
            "Verifique antes de compartilhar.\n\n"
        )

    elif categoria == "SUSPEITO":

        emoji = "🟡"

        alerta = (
            "⚠️ ATENÇÃO!\n"
            "Este conteúdo apresenta alguns sinais suspeitos.\n"
            "Verifique a informação antes de acreditar ou compartilhar.\n\n"
        )

    elif categoria == "BAIXO RISCO":

        emoji = "🟢"

        alerta = (
            "✅ Nenhum sinal crítico foi encontrado.\n\n"
        )
    resposta = (
        f"{emoji} Probabilidade de desinformação: "
        f"{score}%\n\n"

        f"Classificação:\n"
        f"{categoria}\n\n"

        f"{alerta}"

        f"Principais evidências:\n"
        f"{motivos_text}\n"

        f"Explicação:\n"
        f"{explicacao}\n\n"
    )

    if len(fontes) > 0:

        resposta += "Fontes confiáveis:\n\n"

        for fonte in fontes:

            resposta += (
                f"• {fonte['titulo']}\n"
                f"{fonte['url']}\n\n"
            )

    try:

        await status_message.edit_text(
            resposta
        )

    except Exception as e:

        print(
            "Erro ao editar mensagem:",
            e
        )

    # salva no banco
    save_analysis(
        "texto",
        score,
        categoria,
        text
    )

    # alerta do anjo
    if score >= 70:

        user_id = update.effective_user.id

        if user_id in guardian_map:

            guardian_id = guardian_map[user_id]

            await context.bot.send_message(
                chat_id=guardian_id,
                text=(
                    "🚨 ALERTA:\n\n"
                    "Foi detectado um possível "
                    "golpe ou fake news."
                )
            )

async def start(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

        "🤖 Detector de Fake News\n\n"

        "Envie um texto ou imagem para análise."
    )

async def meu_id(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

        f"Seu ID é:\n{update.effective_user.id}"
    )

async def anjo(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) != 1:

        await update.message.reply_text(

            "Use:\n/anjo ID_DO_FAMILIAR"
        )

        return

    guardian_map[
        update.effective_user.id
    ] = context.args[0]

    await update.message.reply_text(

        "✅ Anjo da Guarda cadastrado."
    )

async def handle_text(
        update,
        context):

    text = update.message.text

    urls = extract_urls(text)

    if urls:

        status_message = await update.message.reply_text(

            "🌐 Acessando link encontrado..."
        )

        url = urls[0]

        page_text = extract_text_from_url(
            url
        )

        await status_message.edit_text(

            "🔎 Analisando conteúdo..."
        )

        texto_completo = text

        if len(page_text) > 0:

            texto_completo += "\n\n" + page_text

        await status_message.delete()

        await process_analysis(
            update,
            context,
            texto_completo
        )

    else:

        await process_analysis(
            update,
            context,
            text
        )

async def handle_photo(
        update,
        context):

    photo = update.message.photo[-1]

    file = await photo.get_file()

    file_path = "temp.jpg"

    await file.download_to_drive(file_path)

    status_message = await update.message.reply_text(
        "🖼️ Extraindo texto da imagem..."
    )

    text = pytesseract.image_to_string(

        Image.open(file_path),

        lang="por"
    )

    await status_message.edit_text(
        "🤖 Analisando conteúdo..."
    )

    await status_message.delete()

    await process_analysis(
        update,
        context,
        text
    )

def main():

    init_db()

    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .connect_timeout(30)
        .read_timeout(60)
        .write_timeout(60)
        .pool_timeout(60)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("meu_id", meu_id)
    )

    app.add_handler(
        CommandHandler("anjo", anjo)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text
        )
    )

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            handle_photo
        )
    )

    print("Bot iniciado...")

    app.run_polling()


if __name__ == "__main__":
    main()