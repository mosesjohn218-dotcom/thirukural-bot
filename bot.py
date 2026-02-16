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
# ---------- BOOK I ----------
1: ("கடவுள் வாழ்த்து","The Praise of God"),
2: ("வான் சிறப்பு","The Excellence of Rain"),
3: ("நீத்தார் பெருமை","The Greatness of Ascetics"),
4: ("அறன் வலியுறுத்தல்","Assertion of Virtue"),
5: ("இல்வாழ்க்கை","Household Life"),
6: ("வாழ்க்கைத் துணைநலம்","Life Partner"),
7: ("புதல்வரைப் பெறுதல்","Children"),
8: ("அன்புடைமை","Love"),
9: ("விருந்தோம்பல்","Hospitality"),
10: ("இனியவை கூறல்","Sweet Words"),
11: ("செய்ந்நன்றி அறிதல்","Gratitude"),
12: ("நடுவுநிலைமை","Impartiality"),
13: ("அடக்கமுடைமை","Self-Restraint"),
14: ("ஒழுக்கமுடைமை","Decorum"),
15: ("பிறனில் விழையாமை","Not Coveting"),
16: ("பொறையுடைமை","Forbearance"),
17: ("அழுக்காறாமை","No Envy"),
18: ("வெஃகாமை","No Greed"),
19: ("புறங்கூறாமை","No Backbiting"),
20: ("பயனில சொல்லாமை","No Idle Talk"),
21: ("தீவினையச்சம்","Fear of Evil"),
22: ("ஒப்புரவறிதல்","Duty to Society"),
23: ("ஈகை","Charity"),
24: ("புகழ்","Fame"),
25: ("அருளுடைமை","Compassion"),
26: ("புலால் மறுத்தல்","No Flesh"),
27: ("தவம்","Penance"),
28: ("கூடாவொழுக்கம்","Hypocrisy"),
29: ("கள்ளாமை","No Stealing"),
30: ("வாய்மை","Truth"),
31: ("வெகுளாமை","No Anger"),
32: ("இன்னா செய்யாமை","Non-violence"),
33: ("கொல்லாமை","Non-killing"),
34: ("நிலையாமை","Impermanence"),
35: ("துறவு","Renunciation"),
36: ("மெய்யுணர்தல்","Truth Realization"),
37: ("அவாவறுத்தல்","Ending Desire"),
38: ("ஊழ்","Fate"),

# ---------- BOOK II ----------
39: ("இறைமாட்சி","The Greatness of a King"),
40: ("கல்வி","Learning"),
41: ("கல்லாமை","Ignorance"),
42: ("கேள்வி","Listening"),
43: ("அறிவுடைமை","Wisdom"),
44: ("குற்றங்கடிதல்","Correction of Faults"),
45: ("பெரியாரைத் துணைக்கோடல்","Help of Great Men"),
46: ("சிற்றினம் சேராமை","Avoiding Low Company"),
47: ("தெரிந்துசெயல்வகை","Acting with Thought"),
48: ("வலியறிதல்","Knowing Strength"),
49: ("காலமறிதல்","Knowing Time"),
50: ("இடனறிதல்","Knowing Place"),
51: ("தெரிந்துதெளிதல்","Selection"),
52: ("தெரிந்துவினையாடல்","Employment"),
53: ("சுற்றந்தழால்","Kindred"),
54: ("பொச்சாவாமை","Vigilance"),
55: ("செங்கோன்மை","Justice"),
56: ("கொடுங்கோன்மை","Tyranny"),
57: ("வெருவந்தசெய்யாமை","No Terror"),
58: ("கண்ணோட்டம்","Kindliness"),
59: ("ஒற்றாடல்","Spies"),
60: ("ஊக்கமுடைமை","Energy"),
61: ("மடியின்மை","No Laziness"),
62: ("ஆள்வினையுடைமை","Effort"),
63: ("இடுக்கண் அழியாமை","Hope in Trouble"),

64: ("அமைச்சு","Ministers"),
65: ("சொல்வன்மை","Eloquence"),
66: ("வினைத்தூய்மை","Purity in Action"),
67: ("வினைத்திட்பம்","Firmness"),
68: ("வினைசெயல்வகை","Modes of Action"),
69: ("தூது","Ambassadors"),
70: ("மன்னரைச் சேர்ந்தொழுதல்","Conduct before Kings"),
71: ("குறிப்பறிதல்","Intuition"),
72: ("அவையறிதல்","Council Knowledge"),
73: ("அவையஞ்சாமை","Fearlessness in Council"),
74: ("நாடு","Country"),
75: ("அரண்","Fortress"),
76: ("பொருள்செயல்வகை","Wealth Management"),
77: ("படைமாட்சி","Army Excellence"),
78: ("படைச்செருக்கு","Military Pride"),
79: ("நட்பு","Friendship"),
80: ("நட்பாராய்தல்","Testing Friendship"),
81: ("பழைமை","Old Friendship"),
82: ("தீ நட்பு","Evil Friendship"),
83: ("கூடா நட்பு","False Friendship"),
84: ("பேதைமை","Folly"),
85: ("புல்லறிவாண்மை","Petty Ignorance"),
86: ("இகல்","Enmity"),
87: ("பகைமாட்சி","Power of Enmity"),
88: ("பகைத்திறந்தெரிதல்","Nature of Enmity"),
89: ("உட்பகை","Hidden Enemies"),
90: ("பெரியாரைப் பிழையாமை","Not Offending Great"),
91: ("பெண்வழிச்சேறல்","Led by Women"),
92: ("வரைவின் மகளிர்","Wanton Women"),
93: ("கள்ளுண்ணாமை","No Liquor"),
94: ("சூது","Gambling"),
95: ("மரந்து","Medicine"),

96: ("குடிமை","Nobility"),
97: ("மானம்","Honor"),
98: ("பெருமை","Greatness"),
99: ("சான்றாண்மை","Perfect Character"),
100: ("பண்புடைமை","Courtesy"),
101: ("நன்றியில் செல்வம்","Wealth Misused"),
102: ("நாணுடைமை","Modesty"),
103: ("குடிசெயல்வகை","Family Welfare"),
104: ("உழவு","Agriculture"),
105: ("நல்குரவு","Poverty"),
106: ("இரவு","Begging"),
107: ("இரவச்சம்","Fear of Begging"),
108: ("கயமை","Baseness"),
}

def get_book(n):
    if 1 <= n <= 380:
        return "📘 Aṟattuppāl (Book I – Virtue)"
    elif 381 <= n <= 1080:
        return "📗 Poruḷ (Book II – Wealth / Politics)"
    elif 1081 <= n <= 1330:
        return "📙 Inbam (Book III – Love)"
    return ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📘 Thirukkural Bot\n\n"
        "Send any number 1–1330\n"
        "and explore timeless wisdom ✨"
    )

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text not in kurals:
        await update.message.reply_text("Send a number between 1 and 1330")
        return

    n = int(text)
    chapter = (n - 1) // 10 + 1
    book = get_book(n)
    k = kurals[text]

    msg = f"{book}\n\n"

    if chapter in chapters:
        t, e = chapters[chapter]
        msg += f"Adigaram {chapter}:\n{t}\n{e}\n\n"

    msg += f"📖 Kural {text}\n\n🇮🇳 {k['ta']}\n\n🌍 {k['en']}"

    await update.message.reply_text(msg)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, reply))
app.run_polling()
