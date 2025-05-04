import os
import openai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)
from aiohttp import web

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_DOMAIN = os.getenv("WEBHOOK_DOMAIN")  # например: https://yourapp.up.railway.app
WEBHOOK_PATH = f"/{TELEGRAM_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_DOMAIN}{WEBHOOK_PATH}"

openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте. Меня зовут Алексей — я виртуальный психолог с более чем 15-летним опытом.\n"
        "Я здесь, чтобы вы могли поговорить, получить поддержку и разобраться в том, что вас беспокоит.\n"
        "Расскажите, как вы себя чувствуете сегодня?"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_input = update.message.text

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты — профессиональный психолог с 15-летним опытом. "
                                              "Ты говоришь спокойно, вдумчиво, эмпатично. Ты поддерживаешь, "
                                              "задаёшь уточняющие вопросы и мягко помогаешь разобраться."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response['choices'][0]['message']['content']
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {e}")

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    await app.bot.set_webhook(WEBHOOK_URL)

    async def handler(request):
        data = await request.json()
        update = Update.de_json(data, app.bot)
        await app.process_update(update)
        return web.Response()

    return web.Application().add_routes([web.post(WEBHOOK_PATH, handler)])

if __name__ == "__main__":
    from telegram.ext._utils.io import install_asyncio_event_loop
    install_asyncio_event_loop()
    web.run_app(main(), port=int(os.getenv("PORT", 8000)))
