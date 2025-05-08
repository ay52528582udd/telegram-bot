from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

# توکن ربات از متغیر محیطی گرفته می‌شه
TOKEN = os.getenv("TOKEN")

# آیدی کانال‌های مورد نظر
REQUIRED_CHANNELS = ["@testtttttttttttttt52"]

def start(update: Update, context):
    update.message.reply_text("سلام! من ربات جوین اجباری‌ام. برای ارسال پیام توی گروه، باید توی کانال زیر عضو شی:\n" +
                              "\n".join(REQUIRED_CHANNELS))

def check_membership(update: Update, context):
    message = update.message
    user_id = message.from_user.id
    chat_id = message.chat_id

    # چک کردن عضویت کاربر توی کانال
    for channel in REQUIRED_CHANNELS:
        try:
            member = context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                # اگه کاربر عضو نباشه، پیامش رو پاک کن
                message.delete()
                message.reply_text(
                    f"برای ارسال پیام، باید توی کانال زیر عضو شی:\n" +
                    "\n".join(REQUIRED_CHANNELS) +
                    "\nبعد از عضویت، دوباره پیام بفرست."
                )
                return
        except Exception as e:
            # اگه ربات ادمین کانال نباشه یا خطایی پیش بیاد
            message.reply_text(f"خطا: لطفاً مطمئن شو که من ادمین کانالم. خطا: {e}")
            return

def main():
    # ساخت Updater
    updater = Updater(TOKEN, use_context=True)

    # گرفتن Dispatcher
    dp = updater.dispatcher

    # اضافه کردن دستورات
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, check_membership))

    # اجرای ربات
    print("ربات در حال اجراست...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
