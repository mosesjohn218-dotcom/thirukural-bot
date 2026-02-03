import telegram
from telegram.ext import ApplicationBuilder, MessageHandler, filters

TOKEN = "YOUR_TOKEN_HERE"

async def reply(update, context):
    text = update.message.text
    await update.message.reply_text(f"You said: {text}")

app = ApplicationBuilder().token(TOKEN).build()

handler = MessageHandler(filters.TEXT & ~filters.COMMAND, reply)
app.add_handler(handler)

print("Bot running...")
app.run_polling()
