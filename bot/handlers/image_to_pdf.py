import os
from PIL import Image
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language_map import get_text
from bot.utils.cleanup import cleanup_user_temp

async def start_image_to_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    lang = context.user_data.get("lang", "en")
    context.user_data["image_mode"] = True
    context.user_data["image_paths"] = []

    await query.edit_message_text(get_text(lang, "send_images"))

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")

    if not context.user_data.get("image_mode"):
        return  # ignore if user hasn't started image-to-pdf mode

    user_id = update.effective_user.id
    file = await update.message.photo[-1].get_file()
    os.makedirs(f"/tmp/{user_id}", exist_ok=True)

    image_path = f"/tmp/{user_id}/{file.file_id}.jpg"
    await file.download_to_drive(image_path)

    context.user_data["image_paths"].append(image_path)
    await update.message.reply_text(get_text(lang, "image_received"))

