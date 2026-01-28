import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Берём токен из переменной окружения
TOKEN = os.environ['TELEGRAM_BOT_TOKEN']


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎤 Привет!\n"
        "Пришли текст — я сделаю лингвистический анализ."
    )


async def analyze_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    lines = text.split("\n")
    words = text.split()

    result = (
        f"📊 Анализ текста:\n\n"
        f"Строк: {len(lines)}\n"
        f"Слов: {len(words)}\n"
        f"Среднее слов в строке: {round(len(words)/len(lines), 2)}"
    )

    await update.message.reply_text(result)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyze_text))

    print("✅ Бот запущен")
    app.run_polling()


if __name__ == "__main__":
    main()
