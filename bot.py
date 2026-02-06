import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://www.thirukural.ai/kural/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Send number 1-1330 for Kural (Tamil + English)!')

async def handle_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    num_str = update.message.text.strip()
    try:
        num = int(num_str)
        if not 1 <= num <= 1330:
            await update.message.reply_text('Number must be 1-1330.')
            return
    except ValueError:
        await update.message.reply_text('Send a valid number.')
        return

    try:
        url = f"{BASE_URL}{num}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        # Robust extraction: title has first line, find p tags for content
        title = soup.title.string.strip() if soup.title else f"குறள் {num}"
        
        # All <p> after h1 or main content
        p_tags = soup.find_all('p')
        tamil_lines = []
        eng_line = ""
        for p in p_tags:
            text = p.get_text(strip=True)
            if text and 'அகர' in text or len(tamil_lines) < 2:  # First lines are Tamil
                tamil_lines.append(text)
            elif text and len(text) > 50 and any(e in text.lower() for e in ['the', 'a', 'as']):  # English
                eng_line = text
                break

        tamil = '\n'.join(tamil_lines[:2])
        text = f"**{title}**\n\n**தமிழ்:**\n{tamil}\n\n**English:**\n{eng_line or 'Fetching...'}"
        await update.message.reply_text(text, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error for {num}: {e}")
        await update.message.reply_text(f'Error fetching Kural {num}. Try again.')

if __name__ == '__main__':
    TOKEN = 'YOUR_BOT_TOKEN_HERE'  # Railway uses env var BOT_TOKEN
    if not TOKEN or TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("Set BOT_TOKEN env var!")
        exit(1)
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_number))
    app.run_polling()
