import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import spacy

# Токен бота
TOKEN = os.environ['TELEGRAM_BOT_TOKEN']

# Загружаем Spacy заранее
nlp = spacy.load("ru_core_news_sm")

# Sentiment анализатор — лениво
sentiment_analyzer = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎤 Привет!\n"
        "Пришли текст — я сделаю лингвистический анализ и определю настроение."
    )

async def analyze_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sentiment_analyzer
    text = update.message.text

    # --- Статистика текста ---
    lines = text.split("\n")
    words = text.split()
    avg_words_per_line = round(len(words)/len(lines), 2) if len(lines) > 0 else 0

    # --- Лингвистический анализ ---
    doc = nlp(text)
    pos_counts = {}
    for token in doc:
        pos_counts[token.pos_] = pos_counts.get(token.pos_, 0) + 1

    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "ADJ"]]
    keywords_summary = ", ".join(list(set(keywords))[:10])

    # --- Настроение текста (лениво) ---
    if sentiment_analyzer is None:
        from transformers import pipeline
        sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="cointegrated/rubert-tiny-sentiment"  # лёгкая модель
        )

    sentiment_result = sentiment_analyzer(text[:512])
    sentiment_label = sentiment_result[0]['label']
    sentiment_score = round(sentiment_result[0]['score'], 2)

    # --- Формируем результат ---
    result = (
        f"📊 Анализ текста:\n\n"
        f"Строк: {len(lines)}\n"
        f"Слов: {len(words)}\n"
        f"Среднее слов в строке: {avg_words_per_line}\n\n"
        f"📝 Части речи (кол-во): {pos_counts}\n"
        f"🔑 Ключевые слова: {keywords_summary}\n\n"
        f"😊 Настроение текста: {sentiment_label} (уверенность {sentiment_score})"
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
