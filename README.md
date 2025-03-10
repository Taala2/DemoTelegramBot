# 🚀 Telegram AI & Crypto Bot

Этот бот работает в Telegram и умеет:
✅ Отвечать на вопросы с помощью AI (ChatGPT)  
✅ Показывать актуальные цены криптовалют с Binance  

## 📌 Функции
- **AI-помощник** – отвечает на вопросы, используя OpenAI API  
- **Отслеживание цен** – получает курсы криптовалют (BTC, ETH и др.) с Binance API  

## 🔧 Установка и запуск

### 1️⃣ Установите зависимости
```bash
pip install -r requirements.txt
```

**Создайте файл .env с токенами**
TG_TOKEN=ваш_токен_бота
AI_TOKEN=ваш_токен_openai

**Запустите бота**
```bash
python bot.py
```
📦 Используемые технологии
Python 3.10+
Aiogram 3 (асинхронный Telegram-бот)
OpenAI API (интеграция с AI)
Binance API (отслеживание цен)
AsyncIO (асинхронная обработка запросов)
