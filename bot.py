import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("❌ Переменная TELEGRAM_BOT_TOKEN не задана")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет!\n"
        "Отправь мне любой текст — я отвечу 😊"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    words = len(text.split())
    chars = len(text)

    await update.message.reply_text(
        f"📊 Анализ текста:\n"
        f"Символов: {chars}\n"
        f"Слов: {words}"
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("✅ Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
