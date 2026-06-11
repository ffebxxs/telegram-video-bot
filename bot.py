import telebot

TOKEN = "8864599968:AAG4z97tu5oagVpEwJWcssswplQiXEnjyVU"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):

    args = message.text.split()

    if len(args) > 1:

        if args[1] == "video1":
            bot.send_message(
                message.chat.id,
                "Video 1 berhasil dipanggil"
            )

        elif args[1] == "video2":
            bot.send_message(
                message.chat.id,
                "Video 2 berhasil dipanggil"
            )

    else:
        bot.send_message(
            message.chat.id,
            "Bot aktif."
        )

bot.infinity_polling()
