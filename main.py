import os
from telegram import Update, File
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from flask import Flask, send_from_directory
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN")
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
app = Flask(name)
@app.route('/files/<path:filename>')
def serve_file(filename):
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    tg = msg.document or msg.video or msg.audio or msg.voice or (msg.photo and msg.photo[-1])
    if not tg:
        await msg.reply_text("✅ فقط فایل پشتیبانی شده ارسال/فوروارد کن")
        return
    file_obj: File = await tg.get_file()
    fname = tg.file_name if hasattr(tg, 'file_name') else msg.message_id
    path = os.path.join(DOWNLOAD_DIR, fname)
    await file_obj.download_to_drive(path)
    link = f"{os.getenv('RENDER_EXTERNAL_URL')}/files/{fname}"
    await msg.reply_text(f"✅ لینک مستقیم فایل:\n{link}")

if name == "main":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8000)).start()
    bot = ApplicationBuilder().token(BOT_TOKEN).build()
    bot.add_handler(MessageHandler(filters.ALL, handle_file))
    bot.run_polling()
