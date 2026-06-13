import telebot
import json
import os
import logging

# =========================

# CONFIG

# =========================

TOKEN = "TOKEN_BARU_KAMU"
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

```
try:
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
except:
    return {}
```

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

    bot.send_message(
        message.chat.id,
        """
```

⚠️ Anda harus bergabung terlebih dahulu.

Channel:
https://t.me/enakkinajaa

Group:
https://t.me/enakkann

Setelah join, buka kembali link video.
"""
)
return

```
bot.send_video(
    message.chat.id,
    videos[video_key]
)
```

# =========================

# RUN BOT

# =========================

print("BOT RUNNING...")

bot.infinity_polling(
skip_pending=True,
timeout=60,
long_polling_timeout=60
)
