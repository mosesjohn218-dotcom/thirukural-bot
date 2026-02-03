import json
import requests
from telegram.ext import ApplicationBuilder, MessageHandler, filters

TOKEN = "8263308419:AAFDuAkJ7PB6WNosUJb-ogshnkHc3_uW0B4"

URL = "https://raw.githubusercontent.com/captn3m0/thirukkural/master/thirukkural.json"

data = requests.get(URL).json()
kurals = {str(k["Number"]): k for k in data}

async def reply(update, context):
    text = update.message.text.strip()

    if text in kurals:
        k = kurals[text]
        msg = f"Kural {text}\n\nTamil:\n{k['Line1']} {k['Line2']}\n\nEnglish:\n{k['Translation']}"
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text("Send a number between 1 and 1330")

app = ApplicationBuilder().token(TOKEN).build()
handler = MessageHandler(filters.TEXT & ~filters.COMMAND, reply)
app.add_handler(handler)

print("Bot running...")
app.run_polling()
