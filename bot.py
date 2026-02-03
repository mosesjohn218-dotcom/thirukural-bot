import os
import requests
from telegram.ext import ApplicationBuilder, MessageHandler, filters

TOKEN = os.getenv("TOKEN")

print("Loading kurals...")
kurals = requests.get(
    "https://raw.githubusercontent.com/selva86/datasets/master/thirukkural.json"
).json()

print("Loaded:", len(kurals))

async def reply(update, context):
    text = update.message.text.strip()

    if text in kurals:
        k = kurals[text]
        msg = f"Kural {text}\n\nTamil:\n{k['Tamil']}\n\nEnglish:\n{k['English']}"
        await update.message.reply_text(msg)
        return

    await update.message.reply_text("Send a number between 1 and 1330")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("Bot running...")
app.run_polling()
