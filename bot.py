import json
from telegram.ext import ApplicationBuilder, MessageHandler, filters

TOKEN = "8263308419:AAFDuAkJ7PB6WNosUJb-ogshnkHc3_uW0B4"

with open("kurals.json", "r", encoding="utf-8") as f:
    kurals = json.load(f)

async def reply(update, context):
    text = update.message.text.strip()

    if text in kurals:
        k = kurals[text]
        msg = f"Kural {text}\n\nTamil:\n{k['ta']}\n\nEnglish:\n{k['en']}"
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text("Send a valid kural number")

app = ApplicationBuilder().token(TOKEN).build()
handler = MessageHandler(filters.TEXT & ~filters.COMMAND, reply)
app.add_handler(handler)

print("Bot running...")
app.run_polling()
