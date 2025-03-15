import telebot

# Replace 'YOUR_API_KEY' with your actual Telegram bot API key
API_KEY = "YOUR_API_KEY"
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(
        message, "Welcome to the Demo Telegram Bot! How can I assist you today?"
    )


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


if __name__ == "__main__":
    bot.polling()
