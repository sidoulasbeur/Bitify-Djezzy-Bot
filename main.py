import telebot
import os
import time

TOKEN = "7912768752:AAGOQXShc3-KJ0DUMaPSvtfhKqZK-_WLViM"
ADMIN_ID = 6935979651  # ضع هنا آي دي الأدمن الذي تصله الأرقام

bot = telebot.TeleBot(TOKEN)

# قاعدة بيانات بسيطة لحفظ الأرقام والمحاولات
users = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "أهلاً بك! أرسل رقم جيزي للتسجيل.")

@bot.message_handler(func=lambda m: True)
def get_number(message):
    user_id = message.from_user.id
    text = message.text.strip()

    # تحقق هل النص رقم
    if not text.isdigit():
        bot.reply_to(message, "❌ من فضلك أرسل رقماً صحيحاً.")
        return

    now = time.time()
    if user_id in users:
        user_data = users[user_id]
        attempts = user_data['attempts']
        last_time = user_data['last_time']

        if attempts >= 2 and now - last_time < 300:
            wait = int(300 - (now - last_time))
            bot.reply_to(message, f"⏳ أعد المحاولة بعد {wait} ثانية.")
            return

        # تحديث عدد المحاولات والوقت
        if now - last_time > 300:
            attempts = 0  # إعادة المحاولات بعد 5 دقائق

        users[user_id] = {
            'attempts': attempts + 1,
            'last_time': now
        }
    else:
        users[user_id] = {
            'attempts': 1,
            'last_time': now
        }

    # أرسل الرقم إلى الأدمن
    bot.send_message(ADMIN_ID, f"📥 رقم جديد من {message.from_user.first_name}:\n`{text}`", parse_mode='Markdown')
    bot.reply_to(message, "✅ تم تسجيل رقمك بنجاح.")

bot.polling()
