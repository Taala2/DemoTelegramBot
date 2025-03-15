# 🤖 Telegram AI & Crypto Bot  

A multifunctional Telegram bot with artificial intelligence and cryptocurrency tracking.  

## ✨ Features  

### 🧠 AI Assistant  
- **Multiple AI Models**  
  - DeepSeek - an advanced language model  
  - Gemini - the latest model from Google  
- **Chat Modes**  
  - 👨‍🔬 Expert - provides detailed analytical responses  
  - 😄 Humorist - responds with humor and creativity  
- **Smart Features**  
  - Conversation context saving  
  - Request limit (50 per day)  
  - Token overload protection  

### 📈 Cryptocurrency Tracker  
- Real-time prices from Binance  
- Supported trading pairs:  
  - BTC, ETH, BNB, XRP, ADA  
  - SOL, DOT, DOGE, MATIC, LTC  
  - LINK, BUSD, VET, XLM, TRX  
- Data caching for fast responses  

## 🚀 Quick Start  

### Prerequisites  
- Python 3.10 or higher  
- PostgreSQL  
- Git  

### Installation  

1. Clone the repository:  
```bash
git clone https://github.com/Taala2/DemoTelegramBot.git
cd telegram-ai-crypto-bot
```

2. Create a virtual environment:  
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:  
```bash
pip install -r requirements.txt
```

4. Set up environment variables:  
Create a `.env` file in the root directory:  
```env
# Tokens  
TG_TOKEN=your_telegram_bot_token  
AI_TOKEN=your_openai_token  
DEEPSEEK=your_deepseek_token  
GEMINI=your_gemini_token  

# Database  
SQLALCHEMY=postgresql+asyncpg://user:password@localhost/dbname  
```

5. Run the bot:  
```bash
python run.py
```

## 🛠 Tech Stack  

### Core Technologies  
- **Python 3.10+** - main programming language  
- **Aiogram 3** - asynchronous framework for Telegram bots  
- **SQLAlchemy** - ORM for database management  
- **PostgreSQL** - main database  
- **AsyncIO** - asynchronous programming  

### API Integrations  
- OpenAI API - for AI model interaction  
- Binance API - for fetching cryptocurrency prices  

## 📊 Architecture  

### Modules  
- `app/handler.py` - bot command handlers  
- `app/utils.py` - utility functions  
- `app/allapi/` - external API integrations  
- `app/database/` - database interactions  

## 👥 Support  
If you encounter any issues, create an issue in the project repository.  