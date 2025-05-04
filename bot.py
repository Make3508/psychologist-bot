from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(
  api_key = OPENAI_API_KEY
)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте. Меня зовут Аскар — я виртуальный психолог с более чем 15-летним опытом.\n"
        "Я здесь, чтобы вы могли поговорить, получить поддержку и разобраться в том, что вас беспокоит.\n"
        "Расскажите, как вы себя чувствуете сегодня?"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Ты — профессиональный психолог с 15-летним опытом. "
                                          "Ты говоришь спокойно, вдумчиво, эмпатично. Ты поддерживаешь, "
                                          "задаёшь уточняющие вопросы и мягко помогаешь разобраться."},
            {"role": "user", "content": user_input},
        ],
    )
    reply = response.choices[0].message.content
  except Exception as e:
    logger.error(f"Ошибка OpenAI: {e}")
    reply = "Извините, произошла ошибка при обращении к психологу. Попробуйте позже."
  await update.message.reply_text(reply)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
app.run_polling()
