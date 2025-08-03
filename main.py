from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "اینجا_توکن_ربات_رو_مستقیم_بذار"  # یا از os.getenv استفاده کن اگر در Render ست کردی

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ ربات فعال است.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text:
        await update.message.reply_text(f"📩 متن شما: {update.message.text}")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

app.run_polling()
