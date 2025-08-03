from flask import Flask, send_from_directory
from telegram.ext import Updater, MessageHandler, Filters
import os

# توکن ربات (مستقیماً اینجا قرار گرفته، می‌تونی از متغیر محیطی هم بخونی)
BOT_TOKEN = "توکن_اینجا_بذار"

# پوشه ذخیره فایل‌ها
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ربات تلگرام
updater = Updater(BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

def handle_file(update, context):
    file = update.message.document or update.message.video
    if not file:
        update.message.reply_text("❌ فایل پشتیبانی نمی‌شود.")
        return

    file_obj = context.bot.get_file(file.file_id)
    filename = file.file_name or f"{file.file_unique_id}.bin"
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    file_obj.download(filepath)

    # ساخت لینک مستقیم از سرور
    base_url = os.getenv("RENDER_EXTERNAL_URL", "http://localhost:8000")
    download_link = f"{base_url}/files/{filename}"
    update.message.reply_text(f"✅ لینک مستقیم:\n{download_link}")

# هندل پیام‌ها
dispatcher.add_handler(MessageHandler(Filters.document | Filters.video, handle_file))

# شروع ربات
updater.start_polling()

# سرور Flask برای ارائه فایل‌ها
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ ربات تلگرام آپلودر فعال است!"

@app.route('/files/<path:filename>')
def serve_file(filename):
    return send_from_directory(DOWNLOAD_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
