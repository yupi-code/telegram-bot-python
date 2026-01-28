import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("8307377985:AAH8z8TaCpVq1ihj_gReU3iG6TCOUylsAGM")

# ---------- Команды ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎤 Привет!\n\n"
        "Отправь мне текст (рэп или поэзию), "
        "а я сделаю лингвистический анализ ✍️"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Просто пришли текст.\n"
        "Я посчитаю слова, строки и среднюю длину строки."
    )


# ---------- Анализ текста ----------

async def analyze_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    lines = text.split("\n")
    words = text.split()

    line_count = len(lines)
    word_count = len(words)
    avg_words_per_line = round(word_count / line_count, 2) if line_count else 0

    result = (
        "📊 *Лингвистический анализ*\n\n"
        f"📝 Строк: {line_count}\n"
        f"🔤 Слов: {word_count}\n"
        f"📏 Средняя длина строки: {avg_words_per_line} слов\n\n"
        "Можно использовать эти данные для сравнения\n"
        "рэп-текстов и классической поэзии 🎶📚"
    )

    await update.message.reply_text(result, parse_mode="Markdown")


# ---------- Запуск бота ----------

def main():
    if not TOKEN:
        raise RuntimeError("❌ Не найден TELEGRAM_BOT_TOKEN")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyze_text))

    print("✅ Бот запущен")
    app.run_polling()


if __name__ == "__main__":
    main()
