
import os
import re
from telegram import Update, File
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from flask import Flask, send_from_directory
import threading

# توکن ربات از متغیر محیطی
BOT_TOKEN = os.getenv("BOT_TOKEN")

# مسیر ذخیره‌سازی فایل‌ها
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# راه‌اندازی اپ Flask برای سرو فایل‌ها
app = Flask(__name__)

@app.route('/files/<path:filename>')
def serve_file(filename):
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)

# هندل پیام‌ها
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    tg = msg.document or msg.video or msg.audio or msg.voice or (msg.photo and msg.photo[-1])

    if tg:
        # دانلود فایل از تلگرام
        file_obj: File = await tg.get_file()
        if hasattr(tg, 'file_name') and tg.file_name:
            fname = tg.file_name
        else:
            fname = f"{msg.message_id}.bin"
        local_path = os.path.join(DOWNLOAD_DIR, fname)
        await file_obj.download_to_drive(local_path)

        # ساخت لینک مستقیم برای فایل
        domain = os.getenv('RENDER_EXTERNAL_URL', '').rstrip('/')
        link = f"{domain}/files/{fname}"
        await msg.reply_text(f"✅ لینک مستقیم فایل:\n{link}")
        return

    # اگر فایل نبود، بررسی لینک پیام تلگرام
    text = (msg.text or "") + " " + (msg.caption or "")
    if re.search(r'https?://t\.me/\S+', text):
        await msg.reply_text(
            "❗️ این فقط یک لینک به پیام تلگرامه.\n"
            "لطفاً خود فایل رو مستقیماً ارسال یا فوروارد کن."
        )
    else:
        await msg.reply_text("📎 لطفاً یک فایل (عکس، ویدیو، سند و...) ارسال یا فوروارد کن.")

# اجرای Flask و ربات به‌صورت موازی
if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8000)).start()
    bot = ApplicationBuilder().token(BOT_TOKEN).build()
    bot.add_handler(MessageHandler(filters.ALL, handle_file))
    bot.run_polling()
