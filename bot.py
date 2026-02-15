import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

with open("kurals.json", encoding="utf-8") as f:
    raw = json.load(f)

kurals = {}
for k in raw["kural"]:
    num = str(k["Number"])
    tamil = k["Line1"] + " " + k["Line2"]
    english = k["Translation"]
    kurals[num] = {"ta": tamil, "en": english}

chapters = {
    1: ("கடவுள் வாழ்த்து", "The Praise of God"),
    2: ("வான் சிறப்பு", "The Excellence of Rain"),
    3: ("நீத்தார் பெருமை", "The Greatness of Ascetics"),
    4: ("அறன் வலியுறுத்தல்", "Assertion of Virtue"),
    5: ("இல்வாழ்க்கை", "Household Life"),
    6: ("வாழ்க்கைத் துணைநலம்", "Life Partner"),
    7: ("புதல்வரைப் பெறுதல்", "Children"),
    8: ("அன்புடைமை", "Love"),
    9: ("விருந்தோம்பல்", "Hospitality"),
    10: ("இனியவை கூறல்", "Sweet Words"),
    11: ("செய்ந்நன்றி அறிதல்", "Gratitude"),
    12: ("நடுவுநிலைமை", "Impartiality"),
    13: ("அடக்கமுடைமை", "Self-Restraint"),
    14: ("ஒழுக்கமுடைமை", "Decorum"),
    15: ("பிறனில் விழையாமை", "Not Coveting"),
    16: ("பொறையுடைமை", "Forbearance"),
    17: ("அழுக்காறாமை", "No Envy"),
    18: ("வெஃகாமை", "No Greed"),
    19: ("புறங்கூறாமை", "No Backbiting"),
    20: ("பயனில சொல்லாமை", "No Idle Talk"),
    21: ("தீவினையச்சம்", "Fear of Evil"),
    22: ("ஒப்புரவறிதல்", "Duty to Society"),
    23: ("ஈகை", "Charity"),
    24: ("புகழ்", "Fame"),
    25: ("அருளுடைமை", "Compassion"),
    26: ("புலால் மறுத்தல்", "No Flesh"),
    27: ("தவம்", "Penance"),
    28: ("கூடாவொழுக்கம்", "Hypocrisy"),
    29: ("கள்ளாமை", "No Stealing"),
    30: ("வாய்மை", "Truth"),
    31: ("வெகுளாமை", "No Anger"),
    32: ("இன்னா செய்யாமை", "Non-violence"),
    33: ("கொல்லாமை", "Non-killing"),
    34: ("நிலையாமை", "Impermanence"),
    35: ("துறவு", "Renunciation"),
    36: ("மெய்யுணர்தல்", "Truth Realization"),
    37: ("அவாவறுத்தல்", "Ending Desire"),
    38: ("ஊழ்", "Fate"),
}

def get_section(ch):
    if 1 <= ch <= 4:
        return "I. Payiraviyal (Preface)"
    elif 5 <= ch <= 24:
        return "II. Illaraiyal (Domestic Virtue)"
    elif 25 <= ch <= 37:
        return "III. Thuravaraiyal (Ascetic Virtue)"
    elif ch == 38:
        return "IV. Oozhiyal (Fate)"
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📘 Thirukkural Bot\n\n"
        "Send a number 1–1330\n"
        "and explore timeless wisdom ✨"
    )

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text not in kurals:
        await update.message.reply_text("Send a number between 1 and 1330")
        return

    n = int(text)
    k = kurals[text]

    msg = ""

    # Only show Book I info if inside 1–380
    if 1 <= n <= 380:
        chapter = (n - 1) // 10 + 1
        section = get_section(chapter)
        t, e = chapters[chapter]

        msg += (
            "📘 Aṟattuppāl (அறத்துப்பால்)\n"
            "Book I – Virtue\n\n"
            f"{section}\n\n"
            f"Adigaram {chapter}:\n"
            f"{t}\n{e}\n\n"
        )

    msg += (
        f"📖 Kural {text}\n\n"
        f"🇮🇳 {k['ta']}\n\n"
        f"🌍 {k['en']}"
    )

    await update.message.reply_text(msg)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, reply))

app.run_polling()
