import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from langdetect import detect

# ====== ТОКЕН ======
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ TELEGRAM_BOT_TOKEN не задан")

# ====== СЛОВАРИ НАСТРОЕНИЯ ======
POSITIVE_WORDS = {
    "хорошо", "отлично", "прекрасно", "классно", "супер",
    "люблю", "рад", "счастлив", "восторг", "круто",
    "замечательно", "офигенно", "приятно"
}

NEGATIVE_WORDS = {
    "плохо", "ужасно", "ненавижу", "грусть", "печально",
    "злой", "бесит", "страшно", "отвратительно", "ужас",
    "кошмар", "раздражает"
}

# ====== КОМАНДА /start ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет!\n\n"
        "Пришли любой текст — я:\n"
        "• определю язык\n"
        "• проанализирую настроение\n"
        "• посчитаю статистику\n"
        "• выделю ключевые слова"
    )

# ====== АНАЛИЗ НАСТРОЕНИЯ ======
def analyze_sentiment(text: str) -> str:
    text = text.lower()
    pos = sum(word in text for word in POSITIVE_WORDS)
    neg = sum(word in text for word in NEGATIVE_WORDS)

    if pos > neg:
        return "😊 Позитивное"
    elif neg > pos:
        return "😠 Негативное"
    else:
        return "😐 Нейтральное"

# ====== КЛЮЧЕВЫЕ СЛОВА ======
def extract_keywords(text: str) -> str:
    words = [
        w.lower().strip(".,!?():;\"'")
        for w in text.split()
        if len(w) > 4
    ]
    unique = list(dict.fromkeys(words))
    return ", ".join(unique[:8]) if unique else "—"

# ====== ОСНОВНОЙ АНАЛИЗ ======
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

# ====== ЗАПУСК ======
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyze_text))

    print("✅ Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
