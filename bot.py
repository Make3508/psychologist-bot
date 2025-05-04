import os
from aiohttp import web
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.environ["BOT_TOKEN"]
PORT = int(os.environ.get("PORT", 8443))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я психолог-бот. Чем могу помочь?")

def setup_webhook(application: Application):
    async def handler(request):
        data = await request.json()
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        return web.Response(text="ok")

    app = web.Application()
    app.router.add_post("/", handler)
    return app


async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    # Set webhook URL from Railway public domain (replace later in real use)
    webhook_url = os.environ.get("WEBHOOK_URL")
    await application.bot.set_webhook(url=webhook_url)

    return setup_webhook(application)

if __name__ == "__main__":
    web.run_app(main(), port=PORT)
