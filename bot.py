import telebot
import json
import os
import logging
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

# =========================

# CONFIG

# =========================

TOKEN = "8864599968:AAG4z97tu5oagVpEwJWcssswplQiXEnjyVU"
ADMIN_ID = 8442594829

CHANNEL_USERNAME = "@enakkinajaa"
GROUP_USERNAME = "@enakkann"

BOT_USERNAME = "enakinajaabot"

DB_FILE = "videos.json"

# =========================

# BOT INIT

# =========================

logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot(TOKEN)

# =========================

# DATABASE

# =========================

def load_videos():
    if not os.path.exists(DB_FILE):
        return {}

    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_videos(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# =========================

# FORCE JOIN CHECK

# =========================

def is_member(user_id):
try:
channel_member = bot.get_chat_member(
CHANNEL_USERNAME,
user_id
)

```
    group_member = bot.get_chat_member(
        GROUP_USERNAME,
        user_id
    )

    channel_ok = channel_member.status in [
        "member",
        "administrator",
        "creator"
    ]

    group_ok = group_member.status in [
        "member",
        "administrator",
        "creator"
    ]

    return channel_ok and group_ok

except Exception as e:
    logging.error(e)
    return False
```

# =========================

# ADMIN COMMAND

# =========================

@bot.message_handler(commands=["id"])
def get_id(message):
bot.reply_to(
message,
f"Your ID: {message.from_user.id}"
)

# =========================

# ADMIN UPLOAD VIDEO

# =========================

@bot.message_handler(content_types=["video"])
def upload_video(message):

```
if message.from_user.id != ADMIN_ID:
    bot.reply_to(
        message,
        "❌ Akses ditolak."
    )
    return

videos = load_videos()

video_key = f"v{len(videos)+1}"

videos[video_key] = message.video.file_id

save_videos(videos)

link = (
    f"https://t.me/"
    f"{BOT_USERNAME}"
    f"?start={video_key}"
)

bot.reply_to(
    message,
    f"""
```

✅ Video berhasil disimpan

Kode: {video_key}

Link:
{link}
"""
)

# =========================

# START COMMAND

# =========================

@bot.message_handler(commands=["start"])
def start(message):

```
args = message.text.split()

if len(args) < 2:
    bot.send_message(
        message.chat.id,
        "👋 Selamat datang."
    )
    return

video_key = args[1]

videos = load_videos()

if video_key not in videos:
    bot.send_message(
        message.chat.id,
        "❌ Video tidak ditemukan."
    )
    return

if not is_member(message.from_user.id):

    markup = InlineKeyboardMarkup()

    btn1 = InlineKeyboardButton(
        "📢 Join Channel",
        url="https://t.me/enakkinajaa"
    )

    btn2 = InlineKeyboardButton(
        "👥 Join Group",
        url="https://t.me/enakkann"
    )

    btn3 = InlineKeyboardButton(
        "🔄 Coba Lagi",
        callback_data=f"check_{video_key}"
    )

    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)

    bot.send_message(
        message.chat.id,
        """
👋 Hello

Anda harus bergabung di Channel/Group saya terlebih dahulu
untuk melihat video yang dibagikan.

Silakan join terlebih dahulu.
""",
        reply_markup=markup
    )

    return

# =========================

# RUN BOT

# =========================
@bot.callback_query_handler(func=lambda call: call.data.startswith("check_"))
def check_join(call):

    video_key = call.data.replace("check_", "")

    if not is_member(call.from_user.id):

        bot.answer_callback_query(
            call.id,
            "❌ Anda belum join."
        )
        return

    videos = load_videos()

    if video_key not in videos:

        bot.answer_callback_query(
            call.id,
            "❌ Video tidak ditemukan."
        )
        return

    bot.answer_callback_query(
        call.id,
        "✅ Verifikasi berhasil"
    )

    bot.send_video(
        call.message.chat.id,
        videos[video_key]
    )
print("BOT RUNNING...")

bot.infinity_polling(
skip_pending=True,
timeout=60,
long_polling_timeout=60
)
