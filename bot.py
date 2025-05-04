import os
import logging
import openai
from aiohttp import web
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Переменные окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_DOMAIN = os.getenv("WEBHOOK_DOMAIN")
PORT = int(os.getenv("PORT", "8000"))

openai.api_key = OPENAI_API_KEY

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Здравствуйте! Я ваш виртуальный психолог. Чем могу помочь?")

# Обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты опытный, сочувствующий психолог с 15-летним стажем. Говори спокойно, доброжелательно и вдумчиво."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=500,
            temperature=0.7
        )
        reply = response['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"Ошибка OpenAI: {e}")
        reply = "Извините, возникла ошибка. Пожалуйста, попробуйте позже."

    await update.message.reply_text(reply)

# Основной запуск
async def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Установка webhook
    webhook_path = f"/webhook/{TELEGRAM_TOKEN}"
    await application.bot.set_webhook(f"{WEBHOOK_DOMAIN}{webhook_path}")

    # aiohttp сервер
    return application.create_app(webhook_path)

# Запуск aiohttp-сервера
if __name__ == "__main__":
    web.run_app(main(), port=PORT)
