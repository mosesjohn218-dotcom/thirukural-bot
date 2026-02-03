import os
from telegram.ext import ApplicationBuilder, MessageHandler, filters

TOKEN = os.getenv("TOKEN")

# TEMP local dataset to prove logic
kurals = {
    "1": {"ta": "அகர முதல எழுத்தெல்லாம்", "en": "A is first of all letters"},
    "2": {"ta": "கற்றதனால் ஆய பயனென்கொல்", "en": "What use is learning"},
    "3": {"ta": "மலர்மிசை ஏகினான்", "en": "Those who reach God"},
    "4": {"ta": "வேண்டுதல் வேண்டாமை", "en": "Desire and freedom"},
    "5": {"ta": "இருள்சேர் இருவினையும்", "en": "Dark deeds vanish"}
}

async def reply(update, context):
    text = update.message.text.strip()

    if text in kurals:
        k = kurals[text]
        msg = f"Kural {text}\n\nTamil:\n{k['ta']}\n\nEnglish:\n{k['en']}"
        await update.message.reply_text(msg)
        return

    await update.message.reply_text("Send a number between 1 and 1330")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("Bot running...")
app.run_polling()
