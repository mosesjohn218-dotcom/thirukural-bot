import os
import json
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

# load kurals
with open("kurals.json", encoding="utf-8") as f:
    raw = json.load(f)

data = raw["kural"]
kurals = {str(k["Number"]): k for k in data}

# ---------- commands ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚡ Thirukkural Bot\n\n"
        "Ancient wisdom. One message away.\n\n"
        "Send any number from 1–1330 to read a kural.\n"
        "Use /random for instant inspiration.\n\n"
        "📖 1330 timeless thoughts\n"
        "💬 In Tamil + English\n"
        "🚀 Always ready."
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "/start – intro\n"
        "/random – random kural\n\n"
        "Or send any number 1–1330."
    )

async def random_kural(update: Update, context: ContextTypes.DEFAULT_TYPE):
    num = str(random.randint(1, 1330))
    await send_kural(update, num)

# ---------- main logic ----------

async def send_kural(update: Update, num: str):
    k = kurals[num]
    tamil = k["Line1"] + " " + k["Line2"]
    english = k["explanation"]

    msg = (
        f"📖 Kural {num}\n\n"
        f"🇮🇳 Tamil:\n{tamil}\n\n"
        f"🌍 English:\n{english}"
    )

    await update.message.reply_text(msg)

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not text.isdigit() or text not in kurals:
        await update.message.reply_text("Send a number between 1 and 1330")
        return

    await send_kural(update, text)

# ---------- app ----------

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("random", random_kural))
app.add_handler(MessageHandler(filters.TEXT, reply))

app.run_polling()
