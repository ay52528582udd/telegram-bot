from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, Filters, ContextTypes
import os

# توکن ربات از متغیر محیطی گرفته می‌شه (برای امنیت)
TOKEN = os.getenv("TOKEN")

# آیدی کانال‌های مورد نظر (فقط یکی دادی، اگه بیشتره اضافه کن)
REQUIRED_CHANNELS = ["@testtttttttttttttt52"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من ربات جوین اجباری‌ام. برای ارسال پیام توی گروه، باید توی کانال زیر عضو شی:\n" +
                                   "\n".join(REQUIRED_CHANNELS))

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user_id = message.from_user.id
    chat_id = message.chat_id

    # چک کردن عضویت کاربر توی کانال
    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                # اگه کاربر عضو نباشه، پیامش رو پاک کن
                await message.delete()
                await message.reply_text(
                    f"برای ارسال پیام، باید توی کانال زیر عضو شی:\n" +
                    "\n".join(REQUIRED_CHANNELS) +
                    "\nبعد از عضویت، دوباره پیام بفرست."
                )
                return
        except Exception as e:
            # اگه ربات ادمین کانال نباشه یا خطایی پیش بیاد
            await message.reply_text(f"خطا: لطفاً مطمئن شو که من ادمین کانالم. خطا: {e}")
            return

async def main():
    # ساخت اپلیکیشن ربات
    app = Application.builder().token(TOKEN).build()

    # اضافه کردن دستورات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(Filters.text & ~Filters.command, check_membership))

    # اجرای ربات
    print("ربات در حال اجراست...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
