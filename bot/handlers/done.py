import os
from PIL import Image
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language_map import get_text
from bot.utils.cleanup import cleanup_user_temp

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")

    if not context.user_data.get("image_mode"):
        await update.message.reply_text(get_text(lang, "no_images_yet"))
        return

    image_paths = context.user_data.get("image_paths", [])
    if not image_paths:
        await update.message.reply_text(get_text(lang, "no_images_yet"))
        return

    try:
        images = [Image.open(p).convert("RGB") for p in image_paths]
        user_id = update.effective_user.id
        output_path = f"/tmp/{user_id}/converted.pdf"

        images[0].save(output_path, save_all=True, append_images=images[1:])

        with open(output_path, "rb") as f:
            await update.message.reply_document(document=f, filename="converted.pdf")

        await update.message.reply_text(get_text(lang, "pdf_ready"))
    except Exception as e:
        await update.message.reply_text("❌ Failed to convert images.")
    finally:
        context.user_data["image_mode"] = False
        context.user_data["image_paths"] = []
        cleanup_user_temp(update.effective_user.id)
