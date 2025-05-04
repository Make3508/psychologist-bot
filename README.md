# Telegram Webhook Psychologist Bot

Вебхук-бот для Railway/Render. Имитирует онлайн-аватара психолога.

## Установка

1. Установите зависимости:
```
pip install -r requirements.txt
```

2. Создайте `.env` с переменными:
- `TELEGRAM_TOKEN`
- `OPENAI_API_KEY`
- `WEBHOOK_DOMAIN` (например, https://yourapp.up.railway.app)

3. Запустите:
```
python bot.py
```

Бот будет слушать вебхуки от Telegram.

## Зависимости

- python-telegram-bot
- openai
- aiohttp
