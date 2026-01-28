from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import re

# Вставь сюда свой токен
TOKEN = "8307377985:AAH8z8TaCpVq1ihj_gReU3iG6TCOUylsAGM"

SLANG = ["че", "чё", "типа", "короче", "бро", "рэп", "бит"]
ARCHAIC = ["чело", "длань", "взор", "перст", "уста", "очи"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 🤖\nОтправь текст, и я составлю лингвистический портрет автора."
    )

async def analyze_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    words = re.findall(r"[а-яё]+", text)
    lines = text.split("\n")

    if not words:
        await update.message.reply_text("Недостаточно текста для анализа 😢")
        return

    word_count = len(words)
    unique_words = len(set(words))
    avg_line_len = sum(len(line.split()) for line in lines) / len(lines)

    slang_count = sum(1 for w in words if w in SLANG)
    archaic_count = sum(1 for w in words if w in ARCHAIC)

    style = "разговорный" if slang_count > archaic_count else "книжный"
    rhythm = "динамичный" if avg_line_len < 6 else "размеренный"
    emotion = "высокая" if unique_words / word_count > 0.6 else "умеренная"
    genre = "современный рэп" if slang_count >= 2 else "классическая поэзия"

    result = (
        "🧩 Лингвистический портрет автора:\n\n"
        f"📌 Стиль речи: {style}\n"
        f"📌 Ритм текста: {rhythm}\n"
        f"📌 Эмоциональная насыщенность: {emotion}\n"
        f"📌 Предполагаемый жанр: {genre}\n\n"
        "📝 Вывод:\n"
        f"Автор использует {style} лексику, текст обладает "
        f"{rhythm} ритмом и {emotion} эмоциональностью, "
        f"что характерно для {genre}."
    )

    await update.message.reply_text(result)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyze_text))
    app.run_polling()

if __name__ == "__main__":
    main()
