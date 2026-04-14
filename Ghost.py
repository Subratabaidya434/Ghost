from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import requests
import os

BOT_TOKEN = "8134071034:AAGaGSd2RilmkKeLy9lbSU8DbXf6TitDi9Y"
API_KEY = "sk_2db2c647691a31db5e06ba74f0341065695f94f195df6188"

VOICE_ID = "EXAVITQu4vr4xnSDxMaL"

async def generate_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

        headers = {
            "xi-api-key": API_KEY,
            "Content-Type": "application/json"
        }

        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.3,
                "similarity_boost": 0.9
            }
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code != 200:
            await update.message.reply_text("❌ Voice generate failed")
            return

        file_name = "voice.mp3"

        with open(file_name, "wb") as f:
            f.write(response.content)

        with open(file_name, "rb") as audio:
            await update.message.reply_voice(audio)

        os.remove(file_name)

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# ❌ asyncio.run() বাদ
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_voice))

print("Bot running with REAL AI voice...")
app.run_polling()
