from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "توکن_ربات_اینجا"  # مثلاً: "81340...."

# وقتی کاربر /start می‌فرسته
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ ربات آماده است.")

# وقتی کاربر متن معمولی می‌فرسته
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text:
        await update.message.reply_text(f"📨 متن شما: {update.message.text}")

# ساخت ربات با توکن
app = ApplicationBuilder().token(BOT_TOKEN).build()

# تعریف دستورات
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# اجرای ربات
app.run_polling()
