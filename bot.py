import os
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

# Load kurals.json
with open("kurals.json", encoding="utf-8") as f:
    raw = json.load(f)

data = raw["kural"]
kurals = {str(k["Number"]): k for k in data}

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text("Send a number between 1 and 1330")
        return

    if text not in kurals:
        await update.message.reply_text("Send a number between 1 and 1330")
        return

    k = kurals[text]

    tamil = k["Line1"] + " " + k["Line2"]
    english = k["explanation"]

    msg = f"Kural {text}\n\nTamil:\n{tamil}\n\nEnglish:\n{english}"
    await update.message.reply_text(msg)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, reply))

app.run_polling()
