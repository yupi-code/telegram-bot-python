import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

from langdetect import detect
from textblob import TextBlob

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ TELEGRAM_BOT_TOKEN не задан")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет!\n"
        "Пришли текст — я сделаю базовый анализ:\n"
        "• язык\n"
        "• настроение\n"
        "• ключевые слова\n"
        "• статистику"
    )

def analyze_sentiment(text: str) -> str:
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.2:
        return "😊 Позитивный"
    elif polarity < -0.2:
        return "😠 Негативный"
    else:
        return "😐 Нейтральный"

def extract_keywords(text: str) -> str:
    words = [
        w.lower().strip(".,!?():;\"'")
        for w in text.split()
        if len(w) > 4
    ]
    keywords = list(dict.fromkeys(words))[:8]
    return ", ".join(keywords) if keywords else "—"

async def analyze_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # статистика
    chars = len(text)
    words_count = len(text.split())

    # язык
    try:
        language = detect(text)
    except:
        language = "не удалось определить"

    # настроение
    sentiment = analyze_sentiment(text)

    # ключевые слова
    keywords = extract_keywords(text)

    await update.message.reply_text(
        f"📊 Анализ текста:\n\n"
        f"🔤 Язык: {language}\n"
        f"😊 Настроение: {sentiment}\n\n"
        f"✍️ Слов: {words_count}\n"
        f"🔡 Символов: {chars}\n\n"
        f"🔑 Ключевые слова:\n{keywords}"
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyze_text))

    print("✅ Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()

