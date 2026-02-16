import os
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

# Load JSON
with open("kurals.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

kurals = {k["Number"]: k for k in raw["kural"]}

# ---------------- BOOK MAPPING ----------------

BOOK_1 = {
    "name": "Book I 📘 Aṟattuppāl (Virtue)",
    "range": (1, 380),
}

BOOK_2 = {
    "name": "Book II 📗 Poruḷ (Wealth / Politics)",
    "range": (381, 1080),
}

BOOK_3 = {
    "name": "Book III 📕 Inbathuppāl (Love)",
    "range": (1081, 1330),
}

# Chapter titles
CHAPTERS = {
1:"கடவுள் வாழ்த்து – The Praise of God",
2:"வான் சிறப்பு – The Excellence of Rain",
3:"நீத்தார் பெருமை – The Greatness of Ascetics",
4:"அறன் வலியுறுத்தல் – Power of Virtue",

5:"இல்வாழ்க்கை – Household Life",
6:"வாழ்க்கைத் துணைநலம் – Worth of a Life Partner",
7:"புதல்வரைப் பெறுதல் – Wealth of Children",
8:"அன்புடைமை – Possession of Love",
9:"விருந்தோம்பல் – Hospitality",
10:"இனியவை கூறல் – Sweet Words",
11:"செய்ந்நன்றி அறிதல் – Gratitude",
12:"நடுவுநிலைமை – Impartiality",
13:"அடக்கமுடைமை – Self Restraint",
14:"ஒழுக்கமுடைமை – Decorum",
15:"பிறனில் விழையாமை – Not Coveting",
16:"பொறையுடைமை – Forbearance",
17:"அழுக்காறாமை – Avoiding Envy",
18:"வெஃகாமை – Avoiding Greed",
19:"புறங்கூறாமை – No Backbiting",
20:"பயனில சொல்லாமை – Idle Words",
21:"தீவினையச்சம் – Fear of Evil",
22:"ஒப்புரவறிதல் – Benevolence",
23:"ஈகை – Charity",
24:"புகழ் – Fame",

25:"அருளுடைமை – Compassion",
26:"புலால் மறுத்தல் – Abstinence from Flesh",
27:"தவம் – Penance",
28:"கூடாவொழுக்கம் – Hypocrisy",
29:"கள்ளாமை – No Stealing",
30:"வாய்மை – Truthfulness",
31:"வெகுளாமை – Avoid Anger",
32:"இன்னா செய்யாமை – Non Violence",
33:"கொல்லாமை – Non Killing",
34:"நிலையாமை – Impermanence",
35:"துறவு – Renunciation",
36:"மெய்யுணர்தல் – Truth Realization",
37:"அவாவறுத்தல் – Desire Removal",
38:"ஊழ் – Fate",

39:"இறைமாட்சி – Greatness of a King",
40:"கல்வி – Learning",
41:"கல்லாமை – Ignorance",
42:"கேள்வி – Listening",
43:"அறிவுடைமை – Wisdom",
44:"குற்றங்கடிதல் – Correction of Faults",
45:"பெரியாரைத் துணைக்கோடல் – Seeking Great Men",
46:"சிற்றினம் சேராமை – Avoid Low Company",
47:"தெரிந்துசெயல்வகை – Acting Carefully",
48:"வலியறிதல் – Knowing Strength",
49:"காலமறிதல் – Right Time",
50:"இடனறிதல் – Right Place",
51:"தெரிந்துதெளிதல் – Confidence",
52:"தெரிந்துவினையாடல் – Employment",
53:"சுற்றந்தழால் – Kindred",
54:"பொச்சாவாமை – Vigilance",
55:"செங்கோன்மை – Justice",
56:"கொடுங்கோன்மை – Tyranny",
57:"வெருவந்தசெய்யாமை – No Terror",
58:"கண்ணோட்டம் – Kindness",
59:"ஒற்றாடல் – Spies",
60:"ஊக்கமுடைமை – Energy",
61:"மடியின்மை – No Laziness",
62:"ஆள்வினையுடைமை – Perseverance",
63:"இடுக்கண் அழியாமை – Hope",

64:"அமைச்சு – Ministers",
65:"சொல்வன்மை – Eloquence",
66:"வினைத்தூய்மை – Pure Action",
67:"வினைத்திட்பம் – Firm Action",
68:"வினைசெயல்வகை – Modes of Action",
69:"தூது – Envoy",
70:"மன்னரைச் சேர்ந்தொழுதல் – Conduct with Kings",
71:"குறிப்பறிதல் – Intuition",
72:"அவையறிதல் – Council Knowledge",
73:"அவையஞ்சாமை – No Fear in Council",
74:"நாடு – Country",
75:"அரண் – Fort",
76:"பொருள்செயல்வகை – Wealth Accumulation",
77:"படைமாட்சி – Army Excellence",
78:"படைச்செருக்கு – Military Pride",
79:"நட்பு – Friendship",
80:"நட்பாராய்தல் – Testing Friends",
81:"பழைமை – Old Friendship",
82:"தீ நட்பு – Evil Friendship",
83:"கூடா நட்பு – False Friendship",
84:"பேதைமை – Folly",
85:"புல்லறிவாண்மை – Petty Wisdom",
86:"இகல் – Hostility",
87:"பகைமாட்சி – Might of Enmity",
88:"பகைத்திறந்தெரிதல் – Nature of Enmity",
89:"உட்பகை – Internal Foes",
90:"பெரியாரைப் பிழையாமை – Respect Great",
91:"பெண்வழிச்சேறல் – Led by Women",
92:"வரைவின் மகளிர் – Wanton Women",
93:"கள்ளுண்ணாமை – No Liquor",
94:"சூது – Gambling",
95:"மரந்து – Medicine",

96:"குடிமை – Nobility",
97:"மானம் – Honor",
98:"பெருமை – Greatness",
99:"சான்றாண்மை – Perfect Character",
100:"பண்புடைமை – Courtesy",
101:"நன்றியில் செல்வம் – Useless Wealth",
102:"நாணுடைமை – Modesty",
103:"குடிசெயல்வகை – Family Welfare",
104:"உழவு – Agriculture",
105:"நல்குரவு – Poverty",
106:"இரவு – Begging",
107:"இரவச்சம் – Fear of Begging",
108:"கயமை – Baseness",

109:"தகையணங்குறுத்தல் – Beauty of Beloved",
110:"குறிப்பறிதல் – Reading Signs",
111:"புணர்ச்சி மகிழ்தல் – Joy of Union",
112:"நலம் புனைந்துரைத்தல் – Praising Beauty",
113:"காதற்சிறப்புரைத்தல் – Love’s Excellence",
114:"நாணுத் துறவுரைத்தல் – Abandoning Shyness",
115:"அலரறிவுறுத்தல் – Rumors of Love",

116:"பிரிவாற்றாமை – Separation Pain",
117:"படர்மெலிந்திரங்கல் – Loneliness",
118:"கண்விதுப்பழிதல் – Languishing Eyes",
119:"பசப்புறு பருவரல் – Pallid Hue",
120:"தனிப்படர் மிகுதி – Solitary Anguish",
121:"நினைந்தொன்றுரைத்தல் – Recall Joys",
122:"கனவுநிலை உரைத்தல் – Dreams",
123:"பொழுதுகண்டு இரங்கல் – Sunset Lament",
124:"உறுப்புநலன் அழிதல் – Beauty Wasting",
125:"நெஞ்சொடு கிளத்தல் – Speak to Heart",
126:"நிறையழிதல் – Loss of Control",
127:"அவர்வயின் விதும்பல் – Longing Return",
128:"குறிப்பறிவுறுத்தல் – Signs of Return",
129:"புணர்ச்சி விதும்பல் – Reunion Desire",
130:"நெஞ்சொடு புலத்தல் – Chide Heart",
131:"புலவி – Lovers Quarrel",
132:"புலவி நுணுக்கம் – Subtle Sulk",
133:"ஊடலுவகை – Pleasure of Reunion",
}

# ---------------- FUNCTIONS ----------------

def get_book(num):
    if num <= 380:
        return BOOK_1
    elif num <= 1080:
        return BOOK_2
    return BOOK_3

def get_chapter(num):
    return ((num - 1) // 10) + 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📜 Welcome to Thirukkural Bot\n\n"
        "Send any number 1–1330 to read a Kural.\n"
        "Instant Tamil + English with chapter info ✨"
    )
    await update.message.reply_text(msg)

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text("Send a number between 1 and 1330")
        return

    num = int(text)

    if num < 1 or num > 1330:
        await update.message.reply_text("Send a number between 1 and 1330")
        return

    k = kurals[num]
    book = get_book(num)
    chapter = get_chapter(num)
    chapter_name = CHAPTERS.get(chapter, "")

    msg = (
        f"{book['name']}\n\n"
        f"Adigaram {chapter}:\n{chapter_name}\n\n"
        f"📖 Kural {num}\n\n"
        f"🇮🇳 {k['Line1']}\n{k['Line2']}\n\n"
        f"🌍 {k['explanation']}"
    )

    await update.message.reply_text(msg)

# ---------------- RUN ----------------

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, reply))

app.run_polling()
