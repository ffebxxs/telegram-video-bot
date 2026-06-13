import telebot
import json
import os

TOKEN = "8864599968:AAG4z97tu5oagVpEwJWcssswplQiXEnjyVU"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 8442594829

CHANNELS = [
    "@nakkinajaa",
    "@enakkann",
    
]

DATA_FILE = "videos.json"

# ======================
# LOAD DATABASE
# ======================
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        videos = json.load(f)
else:
    videos = {}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(videos, f)

# ======================
# CEK JOIN
# ======================
def check_join(user_id):
    for ch in CHANNELS:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status in ["left", "kicked"]:
                return False
        except:
            return False
    return True

# ======================
# START LINK HANDLER
# ======================
@bot.message_handler(commands=['start'])
def start(message):
    args = message.text.split()

    if len(args) == 1:
        bot.send_message(message.chat.id, "Gunakan link dari channel.")
        return

    video_id = args[1].replace("video_", "")

    if not check_join(message.from_user.id):
        markup = telebot.types.InlineKeyboardMarkup()

        for ch in CHANNELS:
            markup.add(
                telebot.types.InlineKeyboardButton(
                    "Join " + ch,
                    url=f"https://t.me/{ch.replace('@','')}"
                )
            )

        markup.add(
            telebot.types.InlineKeyboardButton(
                "🔄 Saya sudah join",
                callback_data=f"check_{video_id}"
            )
        )

        bot.send_message(
            message.chat.id,
            "❌ Kamu harus join semua channel/grup dulu!",
            reply_markup=markup
        )
        return

    send_video(message.chat.id, video_id)

# ======================
# CHECK BUTTON
# ======================
@bot.callback_query_handler(func=lambda call: call.data.startswith("check_"))
def callback_check(call):
    video_id = call.data.split("_")[1]

    if not check_join(call.from_user.id):
        bot.answer_callback_query(call.id, "Kamu belum join semua!")
        return

    send_video(call.message.chat.id, video_id)

# ======================
# SEND VIDEO
# ======================
def send_video(chat_id, video_id):
    if video_id in videos:
        bot.send_video(chat_id, videos[video_id])
    else:
        bot.send_message(chat_id, "Video tidak ditemukan.")

# ======================
# UPLOAD VIDEO ADMIN
# ======================
@bot.message_handler(commands=['upload'])
def upload(message):
    if message.from_user.id != ADMIN_ID:
        return

    msg = bot.send_message(message.chat.id, "Kirim video sekarang...")
    bot.register_next_step_handler(msg, save_video)

def save_video(message):
    if not message.video:
        bot.send_message(message.chat.id, "Itu bukan video.")
        return

    file_id = message.video.file_id

    video_id = str(len(videos) + 1)
    videos[video_id] = file_id
    save_data()

    link = f"https://t.me/{bot.get_me().username}?start=video_{video_id}"

    bot.send_message(message.chat.id, f"✅ Video disimpan!\nLink:\n{link}")

# ======================
bot.polling()
