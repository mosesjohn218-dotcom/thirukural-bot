import os
import json
import tempfile
import threading
from gtts import gTTS
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

TOKEN = os.getenv("TOKEN")

# --------------------------
# Flask web server (for Render)
# --------------------------
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Thirukkural Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)

# --------------------------
# Load kurals
# --------------------------
with open("kurals.json", encoding="utf-8") as f:
    raw = json.load(f)

kurals = {str(k["Number"]): k for k in raw["kural"]}

# --------------------------
# Load adigarams
# --------------------------
with open("adigarams.json", encoding="utf-8") as f:
    adigarams = json.load(f)

# --------------------------
# /start command
# --------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📜 Thirukkural Bot\n\n"
        "Send any number from 1–1330\n"
        "to receive the kural + chapter info.\n\n"
        "🎧 Audio will be included automatically."
    )
    await update.message.reply_text(text)

# --------------------------
# Main reply
# --------------------------
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text("Send a number between 1 and 1330")
        return

    num = int(text)

    if num < 1 or num > 1330:
        await update.message.reply_text("Send a number between 1 and 1330")
        return

    # find chapter
    chapter = ((num - 1) // 10) + 1

    if str(chapter) not in adigarams:
        await update.message.reply_text("Chapter info missing.")
        return

    book, tamil_title, eng_title = adigarams[str(chapter)]

    k = kurals[str(num)]

    tamil = f"{k['Line1']}\n{k['Line2']}"
    english = k["Translation"]

    message = (
        f"{book}\n"
        f"Adigaram {chapter}: {tamil_title} ({eng_title})\n\n"
        f"📖 Kural {num}\n\n"
        f"🇮🇳 {tamil}\n\n"
        f"🌍 {english}"
    )

    await update.message.reply_text(message)

    # --------------------------
    # Generate Tamil audio
    # --------------------------
    try:
        speech = f"{k['Line1']} {k['Line2']}"

        tts = gTTS(speech, lang="ta")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tts.save(tmp.name)
            await update.message.reply_voice(voice=open(tmp.name, "rb"))

    except Exception as e:
        print("Audio error:", e)

# --------------------------
# Run bot
# --------------------------
def main():

    print("Thirukkural Bot is starting...")

    # start Flask web server (for Render port detection)
    threading.Thread(target=run_web).start()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, reply))

    app.run_polling()

if __name__ == "__main__":
    main()
