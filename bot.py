import telegram
from telegram.ext import ApplicationBuilder, MessageHandler, filters

TOKEN = "8263308419:AAFDuAkJ7PB6WNosUJb-ogshnkHc3_uW0B4"

kurals = {
    "1": {
        "ta": "அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு",
        "en": "As the letter A is the first of all letters, so the eternal God is first in the world"
    },
    "2": {
        "ta": "கற்றதனால் ஆய பயனென்கொல் வாலறிவன் நற்றாள் தொழாஅர் எனின்",
        "en": "What use is learning if one does not worship the feet of wisdom"
    },
    "3": {
        "ta": "மலர்மிசை ஏகினான் மாணடி சேர்ந்தார் நிலமிசை நீடுவாழ் வார்",
        "en": "Those who reach the feet of God live long upon earth"
    }
}

async def reply(update, context):
    text = update.message.text.strip()

    if text in kurals:
        k = kurals[text]
        msg = f"Kural {text}\n\nTamil:\n{k['ta']}\n\nEnglish:\n{k['en']}"
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text("Send a number (1-3)")

app = ApplicationBuilder().token(TOKEN).build()

handler = MessageHandler(filters.TEXT & ~filters.COMMAND, reply)
app.add_handler(handler)

print("Bot running...")
app.run_polling()
