import telegram
from telegram.ext import ApplicationBuilder, MessageHandler, filters

TOKEN = "8263308419:AAFDuAkJ7PB6WNosUJb-ogshnkHc3_uW0B4"

async def reply(update, context):
    text = update.message.text
    await update.message.reply_text(f"You said: {text}")

app = ApplicationBuilder().token(TOKEN).build()

handler = MessageHandler(filters.TEXT & ~filters.COMMAND, reply)
app.add_handler(handler)

print("Bot running...")
app.run_polling()
