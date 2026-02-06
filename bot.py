import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text("Send a number between 1 and 1330")
        return

    num = int(text)

    if num < 1 or num > 1330:
        await update.message.reply_text("Send a number between 1 and 1330")
        return

    try:
        url = f"https://api-thirukkural.vercel.app/api?num={num}"
        r = requests.get(url, headers=HEADERS, timeout=10)
        data = r.json()

        tamil = data["line1"] + " " + data["line2"]
        english = data["trans"]

        msg = f"Kural {num}\n\nTamil:\n{tamil}\n\nEnglish:\n{english}"
        await update.message.reply_text(msg)

    except Exception as e:
        print(e)
        await update.message.reply_text("Error fetching kural. Try again.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, reply))

app.run_polling()
