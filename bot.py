import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

with open("kurals.json", encoding="utf-8") as f:
    raw = json.load(f)

# Build lookup: number → kural
kurals = {}
for k in raw["kural"]:
    num = str(k["Number"])
    tamil = k["Line1"] + " " + k["Line2"]
    english = k["Translation"]
    kurals[num] = {"ta": tamil, "en": english}

# Chapter titles (Aṟattuppāl only for now — 1 to 38)
chapters = {
    1: ("கடவுள் வாழ்த்து", "Praise of God"),
    2: ("வான் சிறப்பு", "The Excellence of Rain"),
    3: ("நீத்தார் பெருமை", "The Greatness of Ascetics"),
    4: ("அறன் வலியுறுத்தல்", "The Power of Virtue"),
    5: ("இல்வாழ்க்கை", "Domestic Life"),
    6: ("வாழ்க்கைத்துணை நலம்", "The Worth of a Wife"),
    7: ("மக்கட்பேறு", "The Blessing of Children"),
    8: ("அன்புடைமை", "Possession of Love"),
    9: ("விருந்தோம்பல்", "Hospitality"),
    10: ("இனியவை கூறல்", "Sweet Words"),
    11: ("செய்ந்நன்றி அறிதல்", "Gratitude"),
    12: ("நடுவுநிலைமை", "Impartiality"),
    13: ("அடக்கம் உடைமை", "Self-Control"),
    14: ("ஒழுக்கம் உடைமை", "Good Conduct"),
    15: ("பிறனில் விழையாமை", "Not Coveting Another's Wife"),
    16: ("பொறையுடைமை", "Forbearance"),
    17: ("அழுக்காறாமை", "Freedom from Envy"),
    18: ("வெஃகாமை", "Freedom from Greed"),
    19: ("புறங்கூறாமை", "Against Slander"),
    20: ("பயனில சொல்லாமை", "Avoiding Useless Words"),
    21: ("தீவினையச்சம்", "Fear of Evil Deeds"),
    22: ("ஒப்புரவறிதல்", "Equity"),
    23: ("ஈகை", "Charity"),
    24: ("புகழ்", "Fame"),
    25: ("அருளுடைமை", "Compassion"),
    26: ("புலால் மறுத்தல்", "Abstinence from Flesh"),
    27: ("தவம்", "Penance"),
    28: ("கூடா ஒழுக்கம்", "Hypocrisy"),
    29: ("கள்ளாமை", "Truthfulness"),
    30: ("வெகுளாமை", "Freedom from Anger"),
    31: ("இன்னா செய்யாமை", "Non-violence"),
    32: ("கொல்லாமை", "Not Killing"),
    33: ("நிலையாமை", "Impermanence"),
    34: ("துறவு", "Renunciation"),
    35: ("மெய்யுணர்தல்", "Realization of Truth"),
    36: ("அவா அறுத்தல்", "Curbing Desire"),
    37: ("ஊழ்", "Fate"),
    38: ("அறிவுடைமை", "Wisdom"),
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📘 Thirukkural Bot\n\n"
        "Send any number from 1–1330\n"
        "and receive the kural instantly.\n\n"
        "Simple • Fast • Beautiful ✨"
    )
    await update.message.reply_text(msg)

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text not in kurals:
        await update.message.reply_text("Send a number between 1 and 1330")
        return

    num = int(text)
    chapter = (num - 1) // 10 + 1

    tamil_chap, eng_chap = chapters.get(chapter, ("", ""))

    header = (
        "📘 Aṟattuppāl (அறத்துப்பால்)\n"
        "Book of Virtue\n\n"
        f"Adigaram {chapter} (Chapter {chapter}) : "
        f"{tamil_chap} ({eng_chap})\n\n"
    )

    k = kurals[text]

    msg = (
        header +
        f"📖 Kural {text}\n\n"
        f"🇮🇳 {k['ta']}\n\n"
        f"🌍 {k['en']}"
    )

    await update.message.reply_text(msg)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, reply))

app.run_polling()
