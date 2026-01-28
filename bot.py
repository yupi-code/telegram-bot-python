from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from textblob import TextBlob
from langdetect import detect

TOKEN = "YOUR_BOT_TOKEN"

def analyze_sentiment(text: str):
    try:
        lang = detect(text)
    except:
        lang = "unknown"

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.2:
        mood = "😊 позитивное"
    elif polarity < -0.2:
        mood = "😔 негативное"
    else:
        mood = "😐 нейтральное"

    return mood, polarity, lang


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    mood, polarity, lang = analyze_sentiment(text)

    reply = (
        f"🧠 Анализ сообщения:\n"
        f"Настроение: {mood}\n"
        f"Полярность: {polarity:.2f}\n"
        f"Язык: {lang}"
    )

    await update.message.reply_text(reply)


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
