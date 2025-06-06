import os
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language_map import get_text
from bot.utils.cleanup import cleanup_user_temp
from pdf2image import convert_from_path

async def start_pdf_to_images(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = context.user_data.get("lang", "en")
    await query.edit_message_text(get_text(lang, "send_pdf_for_images"))

async def handle_pdf_for_images(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    document = update.message.document

    if not document.file_name.endswith(".pdf"):
        await update.message.reply_text("❌ Please send a valid PDF file.")
        return

    user_id = update.effective_user.id
    temp_dir = f"/tmp/{user_id}"
    os.makedirs(temp_dir, exist_ok=True)

    input_path = f"{temp_dir}/{document.file_name}"
    file = await document.get_file()
    await file.download_to_drive(input_path)

    try:
        await update.message.reply_text(get_text(lang, "processing"))

        images = convert_from_path(input_path, fmt='jpeg', output_folder=temp_dir)

        for i, img in enumerate(images):
            img_path = f"{temp_dir}/page_{i+1}.jpg"
            img.save(img_path, "JPEG")

            with open(img_path, "rb") as f:
                await update.message.reply_photo(f, caption=f"📄 Page {i+1}")

        await update.message.reply_text(get_text(lang, "pdf_to_images_done"))
    except Exception as e:
        await update.message.reply_text("❌ Failed to convert PDF to images.")
    finally:
        cleanup_user_temp(user_id)
