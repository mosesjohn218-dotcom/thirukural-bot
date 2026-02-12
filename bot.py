import os
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

# load JSON
with open("kurals.json", encoding="utf-8") as f:
    data = json.load(f)

# convert list → dictionary for fast lookup
kurals = {str(k["Number"]): k for k in data["kural"]}

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text("Send a number between 1 and 1330")
        return

    num = int(text)

    if num < 1 or num > 1330:
        await update.message.reply_text("Send a number between 1 and 1330")
        return

    k = kurals[str(num)]

    tamil = k["Line1"] + " " + k["Line2"]
    english = k["explanation"]

    msg = f"Kural {num}\n\nTamil:\n{tamil}\n\nEnglish:\n{english}"

    await update.message.reply_text(msg)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, reply))

app.run_polling()
