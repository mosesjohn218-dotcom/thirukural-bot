import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text("Send a number between 1 and 1330")
        return

    num = int(text)

    if num < 1 or num > 1330:
        await update.message.reply_text("Send a number between 1 and 1330")
        return

    url = f"https://www.thirukural.ai/kural/{num}"

    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        tamil = soup.get_text().split("Tamil")[1].split("English")[0].strip()
        english = soup.get_text().split("English")[1].strip()

        msg = f"Kural {num}\n\nTamil:\n{tamil}\n\nEnglish:\n{english}"
        await update.message.reply_text(msg)

    except:
        await update.message.reply_text("Error fetching kural. Try again.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, reply))

app.run_polling()
