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
    data = json.load(f)

# Convert list → dictionary by number
kurals = {str(k["Number"]): k for k in data}

async def reply(update, context):
    text = update.message.text.strip()

    if text in kurals:
        k = kurals[text]
        msg = f"Kural {text}\n\nTamil:\n{k['Line1']} {k['Line2']}\n\nEnglish:\n{k['Translation']}"
        await update.message.reply_text(msg)
        return

    await update.message.reply_text("Send a number between 1 and 1330")

app = ApplicationBuilder().token(TOKEN).build()
handler = MessageHandler(filters.TEXT & ~filters.COMMAND, reply)
app.add_handler(handler)

print("Bot running...")
app.run_polling()
