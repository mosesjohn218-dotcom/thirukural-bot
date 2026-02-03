import json
import os
import requests
from telegram.ext import ApplicationBuilder, MessageHandler, filters

TOKEN = os.getenv("TOKEN")

DATA_FILE = "kurals.json"
URL = "https://raw.githubusercontent.com/arravindhkumar/thirukkural/master/thirukkural.json"

# Download dataset once
if not os.path.exists(DATA_FILE):
    print("Downloading kurals...")
    r = requests.get(URL)
    with open(DATA_FILE, "wb") as f:
        f.write(r.content)

with open(DATA_FILE, "r", encoding="utf-8") as f:
    kurals = json.load(f)   # <-- no conversion

async def reply(update, context):
    text = update.message.text.strip()

    if text in kurals:
        k = kurals[text]
        msg = f"Kural {text}\n\nTamil:\n{k['ta']}\n\nEnglish:\n{k['en']}"
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text("Send a number between 1 and 1330")

app = ApplicationBuilder().token(TOKEN).build()
handler = MessageHandler(filters.TEXT & ~filters.COMMAND, reply)
app.add_handler(handler)

print("Bot running...")
app.run_polling()
