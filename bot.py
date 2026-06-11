import telebot
import json
import os

TOKEN = "TOKEN_BARU_KAMU"

ADMIN_ID = ADMIN_ID_KAMU

CHANNEL_USERNAME = "@enakkinajaa"
GROUP_USERNAME = "@enakkann"

BOT_USERNAME = "enakinajaabot"

bot = telebot.TeleBot(TOKEN)

DB_FILE = "videos.json"


def load_videos():
    if not os.path.exists(DB_FILE):
        return {}

    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_videos(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


def is_member(user_id):
    try:
        ch = bot.get_chat_member(
            CHANNEL_USERNAME,
            user_id
        )

        gp = bot.get_chat_member(
            GROUP_USERNAME,
            user_id
        )

        ok1 = ch.status in [
            "member",
            "administrator",
            "creator"
        ]

        ok2 = gp.status in [
            "member",
            "administrator",
            "creator"
        ]

        return ok1 and ok2

    except:
        return False


@bot.message_handler(commands=['id'])
def get_id(message):
    bot.reply_to(
        message,
        str(message.from_user.id)
    )


@bot.message_handler(content_types=['video'])
def save_video(message):

    if message.from_user.id != ADMIN_ID:
        bot.reply_to(
            message,
            "Akses ditolak."
        )
        return

    videos = load_videos()

    next_id = f"v{len(videos)+1}"

    videos[next_id] = message.video.file_id

    save_videos(videos)

    link = (
        f"https://t.me/"
        f"{BOT_USERNAME}"
        f"?start={next_id}"
    )

    bot.reply_to(
        message,
        f"✅ Video tersimpan\n\n{link}"
    )


@bot.message_handler(commands=['start'])
def start(message):

    args = message.text.split()

    if len(args) < 2:
        bot.send_message(
            message.chat.id,
            "Selamat datang."
        )
        return

    key = args[1]

    videos = load_videos()

    if key not in videos:
        bot.send_message(
            message.chat.id,
            "Video tidak ditemukan."
        )
        return

    if not is_member(message.from_user.id):

        text = (
            "⚠️ Wajib join terlebih dahulu\n\n"
            "Channel:\n"
            "https://t.me/enakkinajaa\n\n"
            "Grup:\n"
            "https://t.me/enakkann\n\n"
            "Setelah join, buka link kembali."
        )

        bot.send_message(
            message.chat.id,
            text
        )

        return

    bot.send_video(
        message.chat.id,
        videos[key]
    )


bot.infinity_polling()
