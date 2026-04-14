from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import requests

BOT_TOKEN = "8134071034:AAGaGSd2RilmkKeLy9lbSU8DbXf6TitDi9Y"
API_KEY = "YOUR_ELEVENLABS_API_KEY"

VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # default voice (changeable)

async def generate_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            "stability": 0.4,
            "similarity_boost": 0.8
        }
    }

    response = requests.post(url, json=data, headers=headers)

    with open("voice.mp3", "wb") as f:
        f.write(response.content)

    with open("voice.mp3", "rb") as audio:
        await update.message.reply_voice(audio)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_voice))

    print("Bot running with REAL AI voice...")
    app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
