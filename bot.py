import os
import logging
import openai
from aiohttp import web
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Настройка логгера
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Получение токенов и домена из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_DOMAIN = os.getenv("WEBHOOK_DOMAIN")

openai.api_key = OPENAI_API_KEY

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте. Меня зовут Аскар — я виртуальный психолог с более чем 15-летним опытом.\n"
        "Я здесь, чтобы вы могли поговорить, получить поддержку и разобраться в том, что вас беспокоит.\n"
        "Расскажите, как вы себя чувствуете сегодня?"
    )

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Можно заменить на "gpt-4" при наличии доступа
            messages=[
                {"role": "system", "content": "Ты опытный, сочувствующий психолог с 15-летним стажем. Говори спокойно, доброжелательно и вдумчиво. Помогай человеку чувствовать поддержку и понимание."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=500,
            temperature=0.7
        )
        reply = response['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"Ошибка OpenAI: {e}")
        reply = "Извините, произошла ошибка при обращении к психологу. Попробуйте позже."

    await update.message.reply_text(reply)

# Главная функция приложения
async def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Настройка webhook
    webhook_path = f"/webhook/{TELEGRAM_TOKEN}"
    await application.bot.set_webhook(url=f"{WEBHOOK_DOMAIN}{webhook_path}")

    # aiohttp веб-приложение
    app = web.Application()
    app.add_routes([web.post(webhook_path, application.webhook_handler())])
    return app

if __name__ == "__main__":
    web.run_app(main(), port=int(os.environ.get("PORT", 8000)))
